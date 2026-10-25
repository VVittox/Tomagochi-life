import json
import math
from pathlib import Path

from exceptions import SaveFormatError


class Storage:
    VERSION = 2

    @staticmethod
    def save(game, path='save.json') -> None:
        pet = game.pet
        data = {
            'version': Storage.VERSION,
            'pet_type': type(pet).__name__,
            'pet': {
                'name': pet.name,
                'hunger': pet.hunger,
                'mood': pet.mood,
                'energy': pet.energy,
                'is_sleeping': pet.is_sleeping,
                'is_alive': pet.is_alive,
            },
            'clock': {'hour': game.clock.hour},
            'game': {'minutes_toward_tick': game.minutes_toward_tick},
        }
        destination = Path(path)
        destination.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    @staticmethod
    def load(path='save.json'):
        from clock import GameClock
        from game import Game
        from pets import Cat, Dog

        source = Path(path)
        try:
            data = json.loads(source.read_text(encoding='utf-8'))
        except FileNotFoundError:
            raise
        except (json.JSONDecodeError, UnicodeError) as error:
            raise SaveFormatError('Файл сохранения повреждён: некорректный JSON.') from error

        if not isinstance(data, dict) or type(data.get('version')) is not int or data['version'] != 2:
            raise SaveFormatError('Неподдерживаемая версия сохранения (нужна версия 2).')
        types = {'Cat': Cat, 'Dog': Dog}
        cls = types.get(data.get('pet_type')) if isinstance(data.get('pet_type'), str) else None
        if cls is None:
            raise SaveFormatError('Неизвестный тип питомца.')
        values, time, meta = data.get('pet'), data.get('clock'), data.get('game', {})
        if not isinstance(values, dict) or not isinstance(time, dict) or not isinstance(meta, dict):
            raise SaveFormatError('Неправильная структура сохранения.')

        name = values.get('name')
        if not isinstance(name, str) or not name.strip():
            raise SaveFormatError('Имя питомца отсутствует или пустое.')
        for key in ('hunger', 'mood', 'energy'):
            value = values.get(key)
            if type(value) is not int or not 0 <= value <= 10:
                raise SaveFormatError(f'Неверное значение {key}: требуется целое от 0 до 10.')
        for key in ('is_sleeping', 'is_alive'):
            if type(values.get(key)) is not bool:
                raise SaveFormatError(f'Неверное значение {key}: требуется true/false.')
        hour = time.get('hour')
        if (type(hour) not in (int, float) or not math.isfinite(hour)
                or not 0 <= hour < 24
                or not math.isclose(hour * 60, round(hour * 60), abs_tol=1e-8)):
            raise SaveFormatError('Некорректное время: 0 <= hour < 24, с точностью до минуты.')
        partial = meta.get('minutes_toward_tick', 0)
        if type(partial) is not int or not 0 <= partial < 60:
            raise SaveFormatError('Неверное значение minutes_toward_tick.')

        pet = cls(name)
        for key in ('hunger', 'mood', 'energy', 'is_sleeping', 'is_alive'):
            setattr(pet, key, values[key])
        return Game(pet, GameClock(hour), partial)
