class TamagotchiError(Exception):
    pass

class PetError(TamagotchiError):
    pass
class PetTooTiredError(PetError):
    pass


class PetTooHungryError(PetError):
    pass


class PetAsleepError(PetError):
    pass


class PetDeadError(PetError):
    pass


class InvalidNameError(TamagotchiError):
    pass


class InvalidMenuInputError(TamagotchiError):
    pass


class SaveFormatError(TamagotchiError):
    pass


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
