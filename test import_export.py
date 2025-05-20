from EP import login, home, bonus, resources
from models import models
import time
import math

time_delay = 15

#login.login()
home.get_planets()
base_planet = models.search_for_planet(models.planets, "3:147:8")
last_planet = models.search_for_planet(models.planets, "4:137:7")
# price, time_left = bonus.get_importexport()
# if price == 0:
#     time.sleep(time_left + time_delay)
# else:
#     crystal_needed = math.ceil(price / 1.5)
#     bonus.purchase_importexport(base_planet, models.Resources(0, crystal_needed, 0))

buildings, _, _ =resources.get_buildings_and_resources(last_planet)
print(buildings)