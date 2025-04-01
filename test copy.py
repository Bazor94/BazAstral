from services import colonize_planet
from EP import home
from models import planet
from EP import login
from EP import staticstics
import threading
from services import farm_idles
from EP import galaxydata
from config import config

ranks = farm_idles.get_player_ranks()
planet.planets = home.get_planets()
farm_idles.plunder_galaxy(planet.planets[1].id, ranks, 800, 6, 258, 499, 35)
