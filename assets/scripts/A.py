from exceptions import PetAsleepError, PetTooTiredError
 
 
class Pet:
    MIN_VALUE = 0
    MAX_VALUE = 10
 
    def __init__(self, name: str):
        self.name = name
        self.hunger = 5
        self.mood = 5
        self.energy = 5
        self.is_sleeping = False
        self.is_alive = True
 
    def _clamp(self):
        self.hunger = max(self.MIN_VALUE, min(self.MAX_VALUE, self.hunger))
        self.mood = max(self.MIN_VALUE, min(self.MAX_VALUE, self.mood))
        self.energy = max(self.MIN_VALUE, min(self.MAX_VALUE, self.energy))
 
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
            print(f"{self.name} уже бодрствует")
            return
        self.is_sleeping = False
        print(f"{self.name} проснулся")
 
    def __str__(self) -> str:
        status = "спит" if self.is_sleeping else "бодрствует"
        return (
            f"[{self.__class__.__name__}: {self.name}] {status} | "
            f"голод: {self.hunger} | "
            f"настроение: {self.mood} | "
            f"энергия: {self.energy}"
        )