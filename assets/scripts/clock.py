# clock.py

class GameClock:
    def __init__(self):
        # Стартовое время по умолчанию
        self.hour = 12

    def advance(self, hours = 1):
        if hours <= 0:
            raise ValueError("Принимается только положительное время")
            
        self.hour = (self.hour + hours) % 24

    def is_night(self):
        return self.hour >= 22 or self.hour < 6

    def __str__(self):
        if self.hour < 10:
            return f"0{self.hour}:00"
        return f"{self.hour}:00"
