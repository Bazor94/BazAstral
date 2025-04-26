from models import models
from services import colonize_planet
from EP import home
from EP import login
from EP import building
import threading
from services import fleet_service


#login.login()
models.planets = home.get_planets()
#building.create_building(planet.planets[-1].id, "METAL_MINE", 10)


base_planet = models.search_for_planet(models.planets, "3:146:8")
t = threading.Thread(target=colonize_planet.colonize_planet, args= (base_planet, "3:146:10", 390, 10, False))
t.start()
