from EP import login, planet, home, resources
from models import models
import time


home.get_planets()
p = models.search_for_planet(models.planets, "2:154:7")
for i in range(0, 5):
    resources.demolish_building(p, "METAL_MINE")
    resources.demolish_building(p, "CRYSTAL_MINE")
    resources.demolish_building(p, "DEUTERIUM_REFINERY")