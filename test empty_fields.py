from EP import login, planet, home, resources, empire, galaxy
from models import models, calc
import time
from logger import logger
import threading
import threads

home.get_planets()
_, referer = galaxy.get_galaxy_html()
empty_planets = []
for x in range(1, 6):
    print(f'searching in {x} galaxy')
    for y in range(1, 500):
        empty_z, referer = galaxy.get_free_fields(x, y, 7, 9, models.planets[0], referer)
        for z in empty_z:
            print(f'empty planet on {x}:{y}:{z}')
            empty_planets.append(f"{x}:{y}:{z}")


print(empty_planets)
