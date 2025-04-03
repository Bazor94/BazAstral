import models.models
from services import colonize_planet
from EP import home
from EP import login
from EP import building
import threading
from services import fleet_service


# login.login()
models.models.planets = home.get_planets()
#building.create_building(planet.planets[-1].id, "METAL_MINE", 10)


base_planet = models.models.search_for_planet(models.models.planets, "3:160:6")
t = threading.Thread(target=colonize_planet.colonize_planet, args= (base_planet, "2:178:11", 365, 12))
t.start()
t = threading.Thread(target=colonize_planet.colonize_planet, args= (base_planet, "2:338:5", 365, 12))
t.start()
