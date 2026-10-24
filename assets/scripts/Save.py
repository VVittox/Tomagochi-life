import storage

class Pet():

    "Другие методы класса"

    def save(self):
        pet_data = {
            "name": self.name,
            "hunger": self.hunger,
            "mood": self.mood,
            "energy": self.energy,
            "time": self.time,
            "is_sleep": self.is_sleep,
            "is_alive": self.is_alive
        }
        storage.save(pet_data)

    def load(self, id):
        pet_data = storage.load(id)
        if pet_data is None:
            print("Нет файла с таким номером сохранения")
            return

        self.name = pet_data["name"]
        self.hunger = pet_data['hunger']
        self.mood = pet_data['mood']
        self.energy = pet_data['energy']
        self.time = pet_data['time']
        self.is_sleep = pet_data['is_sleep']
        self.is_alive = pet_data['is_alive']

        print("Загрузка успешно завершена")

"Остальной код"