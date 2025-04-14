from EP import login, planet, home, resources
from models import models
import time

# login.login()
home.get_planets()
print(models.planets)
while True:
    for p in models.planets:
        referer_url = resources.get_buildings(p)
        for i in range(0, 5):
            try:
                resources.increase_building(p, "METAL_MINE", referer_url)
            except Exception as e:
                break
        for i in range(0, 5):
            try:
                resources.increase_building(p, "CRYSTAL_MINE", referer_url)
            except Exception as e:
                break

        for i in range(0, 5):
            try:
                resources.increase_building(p, "SOLAR_POWER_PLANT", referer_url)
            except Exception as e:
                break
        for i in range(0, 5):
            try:
                resources.increase_building(p, "DEUTERIUM_REFINERY", referer_url)
            except Exception as e:
                break

    time.sleep(60*60)
