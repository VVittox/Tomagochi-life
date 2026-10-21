import math
from Apart import Pet
from Dpart import InvalidNameError

 
def menu(pet: Pet) -> bool:
     
    pass

def main():
    while True:
        try:
            name = input("Как зовут питомца? ").strip() or "Питомец"
            pet = Pet(name)
            print(f"Создан питомец: {pet.name}")
            if not menu(pet):
                return
            print("Начало новой игры...")
        except (EOFError, KeyboardInterrupt):
            print("\nИгра завершена.")
        

if __name__ == "__main__":
    main()

