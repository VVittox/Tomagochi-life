"""Единые исключения и проверка ввода — из Dpart.py."""


class TamagotchiError(Exception):
    """Ошибка в игре Тамагочи."""


class PetError(TamagotchiError):
    """Действие питомца невозможно."""


class PetTooTiredError(PetError):
    """Не хватает энергии."""


class PetTooHungryError(PetError):
    """Слишком сильный голод."""


class PetAsleepError(PetError):
    """Питомец спит."""


class PetDeadError(PetError):
    """Игра закончена для этого питомца."""


class InvalidNameError(TamagotchiError):
    """Неподходящее имя."""


class InvalidMenuInputError(TamagotchiError):
    """Неподходящий пункт меню."""


class SaveFormatError(TamagotchiError):
    """Повреждённое или несовместимое сохранение."""


def check_name(name: str) -> str:
    if not isinstance(name, str) or not name.strip():
        raise InvalidNameError('Имя питомца не может быть пустым!')
    return name.strip()


def limit_stat(value: int) -> int:
    return max(0, min(10, int(value)))


def check_menu_input(user_input: str, maximum: int = 9) -> int:
    cleaned = user_input.strip()
    if not cleaned.isdigit():
        raise InvalidMenuInputError('Нужно ввести номер пункта меню.')
    number = int(cleaned)
    if not 0 <= number <= maximum:
        raise InvalidMenuInputError(f'Выберите число от 0 до {maximum}.')
    return number
