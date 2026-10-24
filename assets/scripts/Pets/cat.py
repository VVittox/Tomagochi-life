from pets.pet import Pet


class Cat(Pet):
    def play(self):
        super().play()
        self.energy += 1
        self._clamp()
        print(f"{self.name} побегал за лазерной указкой и довольно замурчал! Энергия: {self.energy}")