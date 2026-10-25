import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from clock import GameClock
from exceptions import PetAsleepError, PetTooTiredError, SaveFormatError
from game import Game
from pets import Cat, Dog, Pet
from storage import Storage

ROOT = Path(__file__).resolve().parents[1]


class PetTests(unittest.TestCase):
    def test_cat_and_dog_are_pets(self):
        self.assertIsInstance(Cat('Муся'), Pet)
        self.assertIsInstance(Dog('Бим'), Pet)

    def test_cat_dog_play_is_different(self):
        cat, dog = Cat('Муся'), Dog('Бим')
        with contextlib.redirect_stdout(io.StringIO()):
            cat.play()
            dog.play()
        self.assertEqual(cat.energy, 4)
        self.assertEqual(dog.energy, 2)
        self.assertEqual(cat.hunger, 6)
        self.assertEqual(dog.hunger, 7)

    def test_pet_actions_and_bounds(self):
        cat = Cat('Муся')
        with contextlib.redirect_stdout(io.StringIO()):
            for _ in range(15):
                cat.feed()
        self.assertEqual(cat.hunger, 0)
        self.assertEqual(cat.mood, 10)
        cat._clamp()
        self.assertTrue(all(0 <= x <= 10 for x in (cat.hunger, cat.mood, cat.energy)))

    def test_unsuccessful_play_does_not_give_cat_or_dog_bonus(self):
        for cls in (Cat, Dog):
            pet = cls('Тест')
            pet.energy = 1
            with self.assertRaises(PetTooTiredError):
                pet.play()
            self.assertEqual(pet.energy, 1)
            self.assertEqual(pet.hunger, 5)

    def test_cannot_play_while_asleep(self):
        pet = Cat('Муся')
        with contextlib.redirect_stdout(io.StringIO()):
            pet.sleep()
        with self.assertRaises(PetAsleepError):
            pet.play()

    def test_game_has_pet_and_clock(self):
        game = Game(Dog('Бим'), GameClock())
        self.assertIsInstance(game.pet, Pet)
        self.assertIsInstance(game.clock, GameClock)
        self.assertFalse(hasattr(game.pet, 'hour'))
        self.assertFalse(hasattr(game.pet, 'time'))

    def test_clock_minutes_and_night(self):
        clock = GameClock(21.5)
        clock.advance(1)
        self.assertEqual(clock.display(), '22:30')
        self.assertTrue(clock.is_night())
        clock.advance(2)
        self.assertEqual(clock.display(), '00:30')
        for bad in (0, -1, float('nan'), float('inf'), 1e308, True):
            with self.assertRaises(ValueError):
                clock.advance(bad)

    def test_time_ticking_and_sleep(self):
        game = Game(Cat('Муся'), GameClock())
        with contextlib.redirect_stdout(io.StringIO()):
            game.pass_time(0.5)
            self.assertEqual(game.pet.hunger, 5)
            game.pass_time(0.5)
            self.assertEqual(game.pet.hunger, 6)
            self.assertEqual(game.pet.energy, 4)
            game.apply_action('sleep')
        self.assertEqual(game.pet.energy, 6)
        self.assertEqual(game.pet.hunger, 7)
        self.assertTrue(game.pet.is_sleeping)

    def test_failed_action_does_not_change_time(self):
        game = Game(Cat('Муся'), GameClock())
        with contextlib.redirect_stdout(io.StringIO()):
            game.apply_action('sleep')
        hour_before = game.clock.hour
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(game.apply_action('sleep'))
        self.assertEqual(game.clock.hour, hour_before)
        with self.assertRaises(PetAsleepError):
            game.apply_action('play')
        self.assertEqual(game.clock.hour, hour_before)

    def test_death_stops_time_on_first_fatal_tick(self):
        game = Game(Dog('Бим'), GameClock())
        game.pet.hunger = 9
        with contextlib.redirect_stdout(io.StringIO()):
            game.pass_time(8)
        self.assertFalse(game.pet.is_alive)
        self.assertEqual(game.clock.display(), '13:00')


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'save.json'

    def tearDown(self):
        self.temp.cleanup()

    def test_save_and_load_all_values_and_minutes(self):
        game = Game(Dog('Бим'), GameClock())
        with contextlib.redirect_stdout(io.StringIO()):
            game.apply_action('feed')  # 12:30, partial-hour=30
            game.pass_time(0.25)  # 12:45, partial-hour=45
        Storage.save(game, self.path)
        restored = Storage.load(self.path)
        self.assertIsInstance(restored.pet, Dog)
        self.assertEqual(restored.clock.display(), '12:45')
        self.assertEqual(restored.minutes_toward_tick, 45)
        self.assertEqual(restored.pet.__dict__, game.pet.__dict__)
        with contextlib.redirect_stdout(io.StringIO()):
            restored.pass_time(0.25)
        self.assertEqual(restored.pet.hunger, game.pet.hunger + 1)
        self.assertEqual(restored.clock.display(), '13:00')

    def test_save_load_cat_and_sleep(self):
        game = Game(Cat('Мурка'), GameClock())
        with contextlib.redirect_stdout(io.StringIO()):
            game.apply_action('sleep')
        Storage.save(game, self.path)
        restored = Storage.load(self.path)
        self.assertIsInstance(restored.pet, Cat)
        self.assertTrue(restored.pet.is_sleeping)
        self.assertEqual(restored.pet.energy, 7)

    def test_missing_file_raises_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            Storage.load(self.path)

    def test_broken_json_is_handled(self):
        self.path.write_text('{oops', encoding='utf-8')
        with self.assertRaises(SaveFormatError):
            Storage.load(self.path)

    def test_validation_rejects_unknown_type_and_out_of_range(self):
        game = Game(Dog('Бим'), GameClock())
        Storage.save(game, self.path)
        data = json.loads(self.path.read_text('utf-8'))
        data['pet_type'] = 'Dragon'
        self.path.write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaises(SaveFormatError):
            Storage.load(self.path)
        data['pet_type'] = 'Dog'
        data['pet']['hunger'] = 20
        self.path.write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaises(SaveFormatError):
            Storage.load(self.path)

    def test_fractional_minute_roundtrip(self):
        for minute in (1, 31, 62, 123, 245, 481, 1439):
            game = Game(Cat('Муся'), GameClock(minute / 60))
            Storage.save(game, self.path)
            self.assertEqual(Storage.load(self.path).clock.display(),
                             f'{minute // 60:02d}:{minute % 60:02d}')

    def test_example_playbook_save_without_game_field(self):
        data = {
            'version': 2, 'pet_type': 'Dog',
            'pet': {'name': 'Бим', 'hunger': 5, 'mood': 7, 'energy': 6,
                    'is_sleeping': False, 'is_alive': True},
            'clock': {'hour': 12},
        }
        self.path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        game = Storage.load(self.path)
        self.assertEqual(game.pet.name, 'Бим')
        self.assertEqual(game.minutes_toward_tick, 0)


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dir = Path(self.temp.name)
        for filename in ('main.py', 'game.py', 'clock.py', 'storage.py', 'exceptions.py'):
            shutil.copy2(ROOT / filename, self.dir / filename)
        shutil.copytree(ROOT / 'pets', self.dir / 'pets', ignore=shutil.ignore_patterns('__pycache__'))

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, answers):
        return subprocess.run(
            [sys.executable, 'main.py'], input='\n'.join(answers) + '\n',
            cwd=self.dir, text=True, capture_output=True, encoding='utf-8', timeout=10,
        )

    def test_cli_create_both_save_exit_and_load(self):
        result = self.run_cli(['1', 'Муся', '3', '9', '2', 'Бим', '3', '6', '1.5', '7', '0'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Создан питомец Муся (Cat)', result.stdout)
        self.assertIn('Создан питомец Бим (Dog)', result.stdout)
        self.assertIn('за лазерной указкой', result.stdout)
        self.assertIn('носился за мячом', result.stdout)
        self.assertIn('Игра сохранена!', result.stdout)
        self.assertTrue((self.dir/'save.json').exists())
        result2 = self.run_cli(['1', '0'])
        self.assertEqual(result2.returncode, 0, result2.stderr)
        self.assertIn('Загружен питомец Бим!', result2.stdout)

    def test_broken_save_starts_new_game(self):
        (self.dir / 'save.json').write_text('bad-json', encoding='utf-8')
        result = self.run_cli(['1', '2', 'Бим', '0'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Не удалось загрузить сохранение', result.stdout)
        self.assertIn('Создан питомец Бим', result.stdout)

    def test_wrong_input_does_not_crash(self):
        result = self.run_cli(['нет', '1', '', '1', 'Муся', 'х', '6', '-2', '6', 'abc', '0'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Ошибка', result.stdout)
        self.assertIn('Спасибо за игру!', result.stdout)


if __name__ == '__main__':
    unittest.main()
