class Pet():
    def __init__(self, name):
        self.name = name
        self.hunger = 0
        self.mood = 10
        self.energy = 10
        self.time = 360    # Время в минутах
        self.is_sleep = False
        self.is_alive = True
        
    def __str__(self):
        return f"{self.name}: энергия = {self.energy}, голод = {self.hunger}, настроение = {self.mood}"
        
    def clock(self):
        return f"{self.time // 60 % 24:02d}:{self.time % 60:02d}"

    def pass_time(self, hours = 1.0):
        self.time +=  int(hours*60)
        if hours*10%10 >= 5:
            intervals = int(hours)+1
        else:
            intervals = int(hours)

        if intervals > 0:
            if not self.is_sleep:
                self.hunger = min(10, self.hunger + 1 * intervals)
                self.energy = min(10, self.energy + 1 * intervals)
                self.mood = max(0, self.mood - 1 * intervals)
            else:
                self.energy = min(10, self.energy + 2 * intervals)
                self.hunger = min(10, round(self.hunger + 0.5 * intervals))
                self.mood = min(10, round(self.mood + 0.5 * intervals))

        if self.hunger >= 10:
            print(f"{self.name} умер от голода")
            self.is_alive = False
        elif self.mood <= 0:
            print(f"{self.name} умер от депрессии")
            self.is_alive = False

    def feed(self):
        if self.is_sleep:
            print(f"{self.name} сейчас спит!")
            return
        
        if self.energy >= 2:
            if self.hunger >= 5:
                self.hunger -= 5
                self.energy -= 2
                self.pass_time(0.5)
            elif self.hunger > 0:
                self.hunger = 0
                self.energy -= 2
                self.pass_time(0.5)
            else:
                print(f"{self.name} не голоден!")
        else:
            print(f"У {self.name} нет сил")
            return

    def play(self):
        if self.is_sleep:
            print(f"{self.name} сейчас спит!")
            return

        hour = (self.time//60)%24
        if hour >= 22 or hour < 6:
            print(f"{self.name} ночью хочет спать, а не играть!")
            return

        if self.energy >= 4:
            if self.mood <= 5:
                self.mood += 4
                self.energy -= 4
                self.pass_time(1)
            elif self.mood < 10:
                self.mood = 10
                self.energy -= 4
                self.pass_time(1)
            else:
                print(f"{self.name} и так счастлив!")
        else:
            print(f"У {self.name} нет сил")
            return

    def sleep(self):
        if self.time//60%24 >= 22 or self.time//60%24 < 6:
            print(f"{self.name} лег спать")
            self.is_sleep = True

            time = self.time % 1440
            if time < 360:
                time_sleep = 360 - time
            else:
                time_sleep = (1440 - time) + 360
            
            self.pass_time(time_sleep/60)

            if self.is_alive:
                self.wake_up()

        else:
            print(f"{self.name} не устал")
            return

    def wake_up(self):        
        self.is_sleep = False
        print(f"{self.name} проснулся!")
        print()

def main():
    print("Хотите начать новую игру?")
    while True:
        print()
        flag = input("Введите: ДА/НЕТ: ").strip().upper()
        print()
        if flag == "ДА":
            print("Игра запустилась")
            break
        elif flag == "НЕТ":
            return
        else:
            print("Некорректный ввод, попробуйте снова")

    name = input("Назовите своего питомца: ")
    print()
    print("Вы подтвержадете свой выбор? В дальнейшем имя персонажа изменить будет нельзя!")
    flag = input("Введите: ДА/НЕТ: ").strip().upper()
    print()
    while True:
        if flag == "ДА":
            print(f"Поздравляем вы создали персонажа по имени {name}, хорошей игры!")
            print()
            break                                     
        elif flag == "НЕТ":
            print("Хорошо, попробуем снова")
            name = input("Назовите своего питомца: ")
            print()
            print("Вы подтвержадете свой выбор? В дальнейшем имя персонажа изменить будет нельзя!")
            flag = input("Введите: ДА/НЕТ: ").strip().upper()
            print()
        else:
            print("Некорректный ввод, попробуйте снова")
            flag = input("Введите: ДА/НЕТ: ").strip().upper()
            print()
        

    pet = Pet(name)
    print(pet.clock())
    print(pet)
    print()
    while pet.is_alive:
        print("Выберите действия:")
        print("1) Покормить")
        print("2) Поиграть")
        print("3) Заснуть")
        print("4) Пропустить время")
        print("5) Завершить игру")
        print()
        n = input().strip()

        if n == "1":
            pet.feed()
        elif n == "2":
            pet.play()
        elif n == "3":
            pet.sleep()
        elif n == "4":
            pet.pass_time(float(input("Введите, в часах, сколько именно: ")))
        elif n == "5":
            print("Спасибо, что поиграли в наш проект!")
            t = False
        else:
            print("Некорректный ввод, пожалуйста, вводите те номера, которые указаны в списке!")
            print("Попробуем ещё раз")

        if not pet.is_alive:
            break
        else:
            print()
            print(pet.clock())
            print(pet)
            print()

if __name__ == '__main__':
    main()