from colorama import Fore, Style, init   
from Bpart import Cat, Dog              
from Cpart import GameClock
from Dpart import TamagotchiError        

init(autoreset=True) 
def menu(pet):
    """Показывать меню и выполнять команды, пока игрок не выберет выход."""
    while True:
        if not getattr(pet, "is_alive", True):
            print("Игра окончена. Спасибо за игру!")
            return

        print("\n--- ТАМАГОЧИ ---")
        print("1. Показать состояние")
        print("2. Покормить")
        print("3. Поиграть")
        print("4. Уложить спать")
        print("5. Разбудить")
        print("6. Пропустить время")
        print("0. Выход")

        try:
            choice = input("Выберите действие: ").strip()

            if choice == "1":
                print(pet)
            elif choice == "2":
                pet.feed()
            elif choice == "3":
                pet.play()
            elif choice == "4":
                pet.sleep()
            elif choice == "5":
                pet.wake_up()
            elif choice == "6":
                hours = int(input("Сколько часов пропустить? ").strip())
                if hours <= 0:
                    print("Ошибка: количество часов должно быть больше нуля.")
                    continue
                pet.pass_time(hours)
            elif choice == "0":
                print("Спасибо за игру! Пока!")
                return
            else:
                print("Неверный выбор. Введите номер пункта от 0 до 6.")

        except ValueError:
            print("Ошибка: введите целое число часов.")
        except (EOFError, KeyboardInterrupt):
            print("\nИгра завершена.")
            return
        except Exception as error:
            print(f"Не удалось выполнить действие: {error}")
