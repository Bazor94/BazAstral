from services import colonize_planet
from EP import home
from models import planet
from EP import login
from EP import building
import threading
from services import fleet


# login.login()
planet.planets = home.get_planets()
#building.create_building(planet.planets[-1].id, "METAL_MINE", 10)


base_planet = planet.search_for_planet(planet.planets, "3:160:6")
t = threading.Thread(target=colonize_planet.colonize_planet, args= (base_planet, "2:178:11", 365, 12))
t.start()
t = threading.Thread(target=colonize_planet.colonize_planet, args= (base_planet, "2:338:5", 365, 12))
t.start()
