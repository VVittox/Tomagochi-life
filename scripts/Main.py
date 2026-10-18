import math


# часть D
class PetError(Exception):
    pass

class PetTooTiredError(PetError):
    pass

class PetTooHungryError(PetError):
    pass

class PetAsleepError(PetError):
    pass


# часть A
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
        self._partial_hour = 0.0
        self.is_alive = True

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
            f"время: {self._format_time()}"
        )

    def _format_time(self) -> str:
        total_minutes = round(self.hour * 60) % (24 * 60)
        return f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"

# часть B
    def feed(self):
        if self.is_sleeping:
            raise PetAsleepError(f"{self.name} спит и не может есть")
        self.hunger -= 3
        self.mood += 1
        self._clamp()
        print(f"{self.name} поел. Голод: {self.hunger}")


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


# часть C
    def wants_to_sleep(self, hour: float) -> bool:
        return hour >= 22 or hour < 6

    def pass_time(self, hours: float = 1.0) -> None:
        if not math.isfinite(hours) or hours <= 0:
            raise ValueError("Количество часов должно быть положительным числом.")

        if not self.is_alive:
            print(f"{self.name} уже умер. Начните новую игру.")
            return

        remaining = hours
        elapsed = 0.0
        time_to_next_tick = 1 - self._partial_hour
        while remaining + 1e-9 >= time_to_next_tick:
            self.hour = (self.hour + time_to_next_tick) % 24
            remaining -= time_to_next_tick
            elapsed += time_to_next_tick
            self._partial_hour = 0.0

            self.hunger += 1
            if self.is_sleeping:
                self.energy += 2
            else:
                self.energy -= 1
                self.mood -= 1
            self._clamp()

            if self.hunger >= self.MAX_VALUE:
                self.is_alive = False
                print(f"{self.name} умер от голода.")
            elif self.mood <= self.MIN_VALUE:
                self.is_alive = False
                print(f"{self.name} умер от депрессии.")

            if not self.is_alive:
                break

            if not self.is_sleeping and self.wants_to_sleep(self.hour):
                print(f"{self.name} хочет спать (время {int(self.hour):02d}:00)")
            time_to_next_tick = 1.0

        if self.is_alive and remaining > 1e-9:
            self.hour = (self.hour + remaining) % 24
            self._partial_hour += remaining
            elapsed += remaining

        print(f"Прошло {elapsed:g} ч. Сейчас {self._format_time()}")


# часть E
def menu(pet: Pet) -> bool:
    while True:
        if not pet.is_alive:
            print("\nИгра окончена: питомец умер.")
            print("7. Начать новую игру")
            print("0. Выход")
            try:
                choice = input("Выберите действие: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nИгра завершена.")
                return False
            if choice == "7":
                return True
            if choice == "0":
                print("Спасибо за игру! Пока!")
                return False
            print("Питомец умер. Введите 7 для новой игры или 0 для выхода.")
            continue

        print("\n--- Tamogochi Life! от команды 'I use Arhc BTW' ---")
        print("1. Показать состояние")
        print("2. Покормить")
        print("3. Поиграть")
        print("4. Уложить спать")
        print("5. Разбудить")
        print("6. Пропустить время")
        print("7. Начать новую игру")
        print("0. Выход")

        try:
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
                try:
                    hours = float(input("Сколько часов пропустить? ").strip())
                    pet.pass_time(hours)
                except ValueError as error:
                    print(f"Ошибка: {error}")
            elif choice == "0":
                print("Спасибо за игру! Пока!")
                return False
            elif choice == "7":
                return True
            else:
                print("Неверный выбор. Введите номер пункта от 0 до 7.")
        except PetError as error:
            print(error)

def main():
    while True:
        try:
            name = input("Как зовут питомца? ").strip() or "Питомец"
            pet = Pet(name)
            print(f"Создан питомец: {pet.name}")
            if not menu(pet):
                return
            print("Начало новой игры...")
        except (EOFError, KeyboardInterrupt):
            print("\nИгра завершена.")
        

if __name__ == "__main__":
    main()
