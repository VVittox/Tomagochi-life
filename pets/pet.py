from exceptions import (PetAsleepError, PetDeadError, PetTooTiredError,
                        check_name, limit_stat)


class Pet:
    MIN_VALUE = 0
    MAX_VALUE = 10

    def __init__(self, name: str):
        self.name = check_name(name)
        self.hunger = 5
        self.mood = 5
        self.energy = 5
        self.is_sleeping = False
        self.is_alive = True

    def _clamp(self):
        self.hunger = limit_stat(self.hunger)
        self.mood = limit_stat(self.mood)
        self.energy = limit_stat(self.energy)

    def _check_alive(self):
        if not self.is_alive:
            raise PetDeadError(f'{self.name} больше не может выполнять действия. Начните новую игру.')

    def feed(self) -> bool:
        self._check_alive()
        if self.is_sleeping:
            raise PetAsleepError(f'{self.name} спит и не может есть.')
        self.hunger -= 3
        self.mood += 1
        self._clamp()
        print(f'{self.name} поел. Голод: {self.hunger}')
        return True

    def play(self) -> bool:
        self._check_alive()
        if self.is_sleeping:
            raise PetAsleepError(f'{self.name} спит и не может играть.')
        if self.energy < 2:
            raise PetTooTiredError(f'{self.name} слишком устал для игр.')
        self.mood += 2
        self.energy -= 2
        self.hunger += 1
        self._clamp()
        print(f'{self.name} поиграл. Настроение: {self.mood}')
        return True

    def sleep(self) -> bool:
        self._check_alive()
        if self.is_sleeping:
            print(f'{self.name} уже спит.')
            return False
        self.is_sleeping = True
        print(f'{self.name} лёг спать.')
        return True

    def wake_up(self) -> bool:
        self._check_alive()
        if not self.is_sleeping:
            print(f'{self.name} уже бодрствует.')
            return False
        self.is_sleeping = False
        print(f'{self.name} проснулся.')
        return True

    def on_hour_passed(self) -> None:
        """Последствия каждого полного часа из старого main(Old).py.

        Часы здесь НЕ хранятся: Game вызывает метод при смене времени.
        """
        if not self.is_alive:
            return
        self.hunger += 1
        if self.is_sleeping:
            self.energy += 2
        else:
            self.energy -= 1
            self.mood -= 1
        self._clamp()
        if self.hunger >= self.MAX_VALUE:
            self.is_alive = False
            print(f'{self.name} умер от голода. Игра окончена.')
        elif self.mood <= self.MIN_VALUE:
            self.is_alive = False
            print(f'{self.name} умер от плохого настроения. Игра окончена.')

    def __str__(self) -> str:
        status = 'спит' if self.is_sleeping else 'бодрствует'
        if not self.is_alive:
            status = 'игра окончена'
        return (f'[{self.__class__.__name__}: {self.name}] {status} | '
                f'голод: {self.hunger} | настроение: {self.mood} | '
                f'энергия: {self.energy}')
