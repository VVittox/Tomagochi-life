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