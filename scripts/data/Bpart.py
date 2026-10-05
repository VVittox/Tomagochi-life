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
