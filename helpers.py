import math
from config import config
import time
import unittest


def format_seconds(time_needed):
    minutes = time_needed // 60  # Dzielenie całkowite, aby uzyskać minuty
    seconds = time_needed % 60  # Reszta z dzielenia, aby uzyskać sekundy
    return f"{minutes:02}:{seconds:02}"  # Formatuje w postaci mm:ss


def calculate_distance(x_from, y_from, z_from, x_to, y_to, z_to) -> int:
    if x_from == x_to:
        if y_from == y_to:
            if z_from == z_to:
                return 5
            return 1000 + abs(x_from - x_to) * 5
        return 2700 + abs(y_from - y_to) * 95
    return abs(z_from - z_to) * 20000

def calculate_time(x_from, y_from, z_from, x_to, y_to, z_to, fleet_speed, speed_perc):
    speed_perc = speed_perc / 10 # idioci uzywaja 10 jako 100%
    distance = calculate_distance(x_from, y_from, z_from, x_to, y_to, z_to)

    if distance > 1000:
        distance += 1000
    return round(((35000 / speed_perc) * math.sqrt((distance * 10) / fleet_speed) + 10) / config.server.fleet_speed)

class TestFleetCalculations(unittest.TestCase):
    def test_calculate_speed(self):
        x_from, y_from, z_from = 2, 308, 4
        x_to, y_to, z_to = 2, 32, 16
        fleet_speed = 79920
        speed_perc = 100

        # Obliczanie distance
        distance = calculate_distance(x_from, y_from, z_from, x_to, y_to, z_to)
        
        # Oczekiwana wartość distance
        expected_distance = 28920
        self.assertEqual(distance, expected_distance)

        # Obliczanie time przy użyciu distance
        time = calculate_time(x_from, y_from, z_from, x_to, y_to, z_to, fleet_speed, speed_perc)
        
        # Oczekiwana wartość time
        expected_time = 848

        # Porównanie obliczonego czasu z oczekiwanym
        self.assertEqual(time, expected_time)
