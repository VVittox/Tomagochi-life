from .pet import Pet


class Dog(Pet):
    def feed(self) -> bool:
        super().feed()
        self.mood += 1
        self._clamp()
        print(f'{self.name} виляет хвостом от счастья и облизывается!')
        return True

    def play(self) -> bool:
        super().play()
        self.energy -= 1
        self.hunger += 1
        self._clamp()
        print(f'{self.name} с громким лаем носился за мячом!')
        return True

    def wake_up(self) -> bool:
        did_wake = super().wake_up()
        if did_wake:
            print(f'{self.name} радостно залаял и готов бегать!')
        return did_wake
