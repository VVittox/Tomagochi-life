import math
from pathlib import Path

from clock import GameClock
from exceptions import (PetError, SaveFormatError,
                        TamagotchiError, check_menu_input)
from pets import Cat, Dog, Pet
from storage import Storage

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class _NoColor:
        CYAN = GREEN = YELLOW = RED = RESET_ALL = ''
    Fore = Style = _NoColor()

SAVE_PATH = Path(__file__).resolve().parent / 'save.json'


class Game:

    def __init__(self, pet: Pet, clock: GameClock, minutes_toward_tick: int = 0):
        if not isinstance(pet, Pet) or not isinstance(clock, GameClock):
            raise TypeError('Для Game нужны Pet и GameClock.')
        if type(minutes_toward_tick) is not int or not 0 <= minutes_toward_tick < 60:
            raise ValueError('Неверный счётчик неполного часа.')
        self.pet = pet
        self.clock = clock
        self.minutes_toward_tick = minutes_toward_tick

    def pass_time(self, hours: float = 1.0) -> None:
      
        if (isinstance(hours, bool) or not isinstance(hours, (int, float))
                or not math.isfinite(hours) or hours <= 0):
            raise ValueError('Количество часов должно быть положительным числом.')
        if not math.isfinite(hours * 60):
            raise ValueError('Количество часов слишком велико.')
        minutes = round(hours * 60)
        if minutes <= 0:
            raise ValueError('Минимальный шаг времени — одна минута.')
        if not self.pet.is_alive:
            raise PetError('Игра окончена. Начните новую игру.')
        passed = 0
        while minutes:
            until_tick = 60 - self.minutes_toward_tick
            step = min(minutes, until_tick)
            self.clock.advance(step / 60)
            self.minutes_toward_tick += step
            passed += step
            minutes -= step
            if self.minutes_toward_tick == 60:
                self.minutes_toward_tick = 0
                self.pet.on_hour_passed()
                if not self.pet.is_alive:
                    break
        print(f'Прошло {passed / 60:g} ч. Сейчас {self.clock.display()}')
        if self.pet.is_alive and self.clock.is_night() and not self.pet.is_sleeping:
            print(f'{self.pet.name} хочет спать: уже ночь.')

    def apply_action(self, action: str, hours: float | None = None) -> bool:
      
        if action in ('pass_time', 'wait'):
            self.pass_time(1 if hours is None else hours)
            return True
        actions = {'feed': (self.pet.feed, 0.5),
                   'play': (self.pet.play, 1),
                   'sleep': (self.pet.sleep, 1),
                   'wake_up': (self.pet.wake_up, 0.25)}
        if action not in actions:
            raise ValueError(f'Неизвестное действие: {action}')
        callback, duration = actions[action]
        success = callback()
        if success:
            self.pass_time(duration)
        return success

    def show_status(self) -> None:
        print(Fore.CYAN + str(self.pet) + Style.RESET_ALL)
        print(f'Игровое время: {self.clock.display()}')

    def run(self) -> str:

        while True:
            print('\n' + Fore.CYAN + "--- Tamagotchi Life | I use Arch BTW ---" + Style.RESET_ALL)
            self.show_status()
            if self.pet.is_alive:
                print('1. Показать состояние | 2. Покормить | 3. Поиграть')
                print('4. Уложить спать | 5. Разбудить | 6. Пропустить время')
            print('7. Сохранить | 8. Загрузить | 9. Новая игра | 0. Выход')
            choice_text = input('Выберите действие: ')
            try:
                choice = check_menu_input(choice_text)
                if choice == 0:
                    print('Спасибо за игру! Пока!')
                    return 'exit'
                if choice == 9:
                    return 'new'
                if choice == 7:
                    Storage.save(self, SAVE_PATH)
                    print(Fore.GREEN + 'Игра сохранена!' + Style.RESET_ALL)
                elif choice == 8:
                    loaded = Storage.load(SAVE_PATH)
                    self.pet = loaded.pet
                    self.clock = loaded.clock
                    self.minutes_toward_tick = loaded.minutes_toward_tick
                    print(Fore.GREEN + 'Игра загружена!' + Style.RESET_ALL)
                elif not self.pet.is_alive:
                    print('Игра окончена. Выберите 9 для новой игры или 0 для выхода.')
                elif choice == 1:
                    self.show_status()
                elif choice in (2, 3, 4, 5):
                    names = {2: 'feed', 3: 'play', 4: 'sleep', 5: 'wake_up'}
                    self.apply_action(names[choice])
                elif choice == 6:
                    hours = float(input('Сколько часов пропустить (например 1.5)? ').strip().replace(',', '.'))
                    self.apply_action('wait', hours)
            except FileNotFoundError:
                print(Fore.YELLOW + 'Сохранение ещё не найдено. Сначала сохраните игру.' + Style.RESET_ALL)
            except (ValueError, TamagotchiError, OSError) as error:
                print(Fore.YELLOW + f'Ошибка: {error}' + Style.RESET_ALL)


def create_new_game() -> Game:
    while True:
        print('\nВыберите питомца: 1 — Кошка, 2 — Собака')
        answer = input('Ваш выбор: ').strip()
        if answer not in ('1', '2'):
            print('Введите 1 или 2.')
            continue
        name = input('Как зовут питомца? ').strip()
        cls = Cat if answer == '1' else Dog
        try:
            pet = cls(name)
        except TamagotchiError as error:
            print(f'Ошибка: {error}')
            continue
        print(f'Создан питомец {pet.name} ({cls.__name__})!')
        return Game(pet, GameClock())


def main() -> None:
    print("Tamagotchi Life — игра команды 'I use Arch BTW'")
    game = None
    try:
        if SAVE_PATH.is_file():
            print('Найдено сохранение. 1 — загрузить, 2 — новая игра')
            choice = input('Ваш выбор: ').strip()
            if choice == '1':
                try:
                    game = Storage.load(SAVE_PATH)
                    print(f'Загружен питомец {game.pet.name}!')
                except (SaveFormatError, OSError) as error:
                    print(f'Не удалось загрузить сохранение: {error}')
                    print('Можно начать новую игру.')
        if game is None:
            game = create_new_game()
        while game.run() == 'new':
            game = create_new_game()
    except (EOFError, KeyboardInterrupt):
        print('\nИгра завершена.')


if __name__ == '__main__':
    main()
