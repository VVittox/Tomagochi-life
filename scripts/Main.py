#D
class PetError(Exception):
    pass

class PetTooTiredError(PetError):
    pass

class PetTooHungryError(PetError):
    pass

class PetAsleepError(PetError):
    pass

#A
class Pet:
    MIN_VALUE = 0
    MAX_VALUE = 10

    def __init__(self, name: str):
        self.name = name
        self.hunger = 5
        self.mood = 5
        self.energy = 5
        self.is_sleeping = False
        self.hour = 12

    def _clamp(self):
        self.hunger = max(self.MIN_VALUE, min(self.MAX_VALUE, self.hunger))
        self.mood = max(self.MIN_VALUE, min(self.MAX_VALUE, self.mood))
        self.energy = max(self.MIN_VALUE, min(self.MAX_VALUE, self.energy))

    def __str__(self) -> str:
        status = "спит" if self.is_sleeping else "бодрствует"
        return (
            f"[{self.name}] {status} | "
            f"голод: {self.hunger} | "
            f"настроение: {self.mood} | "
            f"энергия: {self.energy} | "
            f"время: {self.hour}:00"
        )

    def feed(self):
        if self.is_sleeping:
            raise PetAsleepError(f"{self.name} спит и не может есть")
        self.hunger -= 3
        self.mood += 1
        self._clamp()
        print(f"{self.name} поел. Голод: {self.hunger}")

#B
    def play(self):
        if self.is_sleeping:
            raise PetAsleepError(f"{self.name} спит и не может играть")
        if self.energy < 2:
            raise PetTooTiredError(f"{self.name} слишком устал для игр")
        self.mood += 2
        self.energy -= 2
        self.hunger += 1
        self._clamp()
        print(f"{self.name} поиграл. Настроение: {self.mood}")

    def sleep(self):
        if self.is_sleeping:
            print(f"{self.name} уже спит")
            return
        self.is_sleeping = True
        print(f"{self.name} лёг спать")

    def wake_up(self):
        if not self.is_sleeping:
            print(f"{self.name} уже не спит")
            return
        self.is_sleeping = False
        print(f"{self.name} проснулся")

#C
    def wants_to_sleep(self, hour):
        return hour >= 22 or hour < 6

    def pass_time(self, hours=1.0):
        self.hour = (self.hour + hours) % 24

        intervals = int(hours)

        if hours - intervals >= 0.5:
            intervals += 1

        if intervals > 0:
            if not self.is_sleeping:
                self.hunger = min(10, self.hunger + intervals)
                self.energy = max(0, self.energy - intervals)
                self.mood = max(0, self.mood - intervals)
            else:
                self.energy = min(10, self.energy + 2 * intervals)
                self.hunger = min(10, round(self.hunger + 0.5 * intervals))
                self.mood = min(10, round(self.mood + 0.5 * intervals))

        if self.hunger >= 10:
            print(f"{self.name} умер от голода")
            self.is_alive = False
        elif self.mood <= 0:
            print(f"{self.name} умер от депрессии")
            self.is_alive = False

#E
def menu(pet):
    """Показывать меню и выполнять команды, пока игрок не выберет выход."""
    while True:
        if not getattr(pet, "is_alive", True):
            print("Игра окончена. Спасибо за игру!")
            return

        print("\n--- ТАМАГОЧИ ---")
        print("1. Показать состояние")
        print("2. Покормить")
        print("3. Поиграть")
        print("4. Уложить спать")
        print("5. Разбудить")
        print("6. Пропустить время")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            print(pet)
        elif choice == "2":
            pet.feed()
        elif choice == "3":
            pet.play()
        elif choice == "4":
            pet.sleep()
        elif choice == "5":
            pet.wake_up()
        elif choice == "6":
            hours = int(input("Сколько часов пропустить? ").strip())
            if hours <= 0:
                print("Ошибка: количество часов должно быть больше нуля.")
                continue
            pet.pass_time(hours)
        elif choice == "0":
            print("Спасибо за игру! Пока!")
            return
        else:
            print("Неверный выбор. Введите номер пункта от 0 до 6.")

def main():
    while True:
        try:
            name = input("Как зовут питомца? ").strip() or "Питомец"
            pet = Pet(name)
            print(f"Создан питомец: {pet.name}")
            menu(pet)
            print("Начало новой игры...")
        except ValueError:
                    print("Ошибка: введите целое число часов.")
                    return
        except (EOFError, KeyboardInterrupt):
                    print("\nИгра завершена.")
                    return
        except Exception as error:
                    print(f"Не удалось выполнить действие: {error}")
                    return
        

if __name__ == "__main__":
    main()
