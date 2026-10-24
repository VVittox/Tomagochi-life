saves = []

def save(pet_data):
    saves.append(pet_data)
    print("Сохранение прошло успешно")

def load(id):
    if id >= 0 and id < len(saves):
        print("Начинаем загрузку")
        return saves[id]
    else:
        return None