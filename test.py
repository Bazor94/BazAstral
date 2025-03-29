from services import colonize_planet
from EP import home
from models import planet
from EP import login
from EP import building


# login.login()
planet.planets = home.get_planets()
#building.create_building(planet.planets[-1].id, "METAL_MINE", 10)

colonize_planet.colonize_planet("6:248:6", "6:220:11", 365, 12)