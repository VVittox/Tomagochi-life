"""Игровые часы: перенос и доработка assets/scripts/clock.py."""
import math


class GameClock:
    def __init__(self, start_hour: float = 12):
        if (isinstance(start_hour, bool) or not isinstance(start_hour, (int, float))
                or not math.isfinite(start_hour) or not 0 <= start_hour < 24):
            raise ValueError('Начальное время должно быть от 00:00 до 23:59.')
        minutes = round(start_hour * 60)
        if minutes >= 1440:
            raise ValueError('Начальное время должно быть от 00:00 до 23:59.')
        self._minutes = minutes

    @property
    def hour(self) -> float:
        """Для JSON: 12.5 означает 12:30."""
        return self._minutes / 60

    def advance(self, hours: float) -> None:
        if (isinstance(hours, bool) or not isinstance(hours, (int, float))
                or not math.isfinite(hours) or hours <= 0):
            raise ValueError('Количество часов должно быть положительным числом.')
        if not math.isfinite(hours * 60):
            raise ValueError('Количество часов слишком велико.')
        minutes = round(hours * 60)
        if minutes < 1:
            raise ValueError('Минимальный шаг времени — одна минута.')
        self._minutes = (self._minutes + minutes) % 1440

    def display(self) -> str:
        return f'{self._minutes // 60:02d}:{self._minutes % 60:02d}'

    def is_night(self) -> bool:
        return self._minutes >= 22 * 60 or self._minutes < 6 * 60

    def __str__(self) -> str:
        return self.display()
