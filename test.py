from services import colonize_planet
from EP import home
from models import planet
from EP import login
from EP import building
import threading


# login.login()
planet.planets = home.get_planets()
#building.create_building(planet.planets[-1].id, "METAL_MINE", 10)

t = threading.Thread(target=colonize_planet.colonize_planet, args= ("6:215:11", "6:213:11", 365, 12))
t.start()
t = threading.Thread(target=colonize_planet.colonize_planet, args= ("6:215:11", "6:183:11", 365, 12))
t.start()
