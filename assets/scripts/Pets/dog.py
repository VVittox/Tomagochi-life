class Dog(Pet):
    def __init__(self, name: str):
        super().__init__(name)

    def feed(self):
        super().feed()
        
        self.mood += 1 # собака больше наслаждается
        self._clamp()
        print(f"{self.name} виляет хвостом от счастья и облизывается!")

    def play(self):
        super().play()
        self.energy -= 1
        self.hunger += 1
        self._clamp()
        print(f"{self.name} с громким лаем носился за мячом!") #играет активнеее и сильнее потому устает

    def sleep(self):
        super().sleep()

    def wake_up(self):
        super().wake_up()
        if not self.is_sleeping and self.is_alive:
            print(f"{self.name} радостно залаял, подпрыгнул и готов бегать!")
