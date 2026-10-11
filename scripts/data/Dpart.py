class TamagotchiError(Exception):
    pass

class InvalidNameError(TamagotchiError):
    pass

class InvalidMenuInputError(TamagotchiError):
    pass

class PetTooTiredError(TamagotchiError):
    pass


def check_name(name: str) -> str:
    if not name or name.strip() == "":
        raise InvalidNameError("Имя питомца не может быть пустым!")
    return name.strip()


def limit_stat(value: int) -> int:
    if value < 0:
        return 0
    if value > 10:
        return 10
    return int(value)


def check_menu_input(user_input: str) -> int:
    cleaned = user_input.strip()
    
    if not cleaned.isdigit():
        raise InvalidMenuInputError("Нужно ввести цифру, а не буквы!")
    
    number = int(cleaned)
    if number < 0 or number > 5:
        raise InvalidMenuInputError("Такого пункта меню нет! Выберите от 0 до 5.")
        
    return number


def main():
    pass


if __name__ == '__main__':
    main()
