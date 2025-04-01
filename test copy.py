from services import colonize_planet
from EP import home
from models import planet
from EP import login
from EP import staticstics
import threading
from services import plunder
from EP import galaxydata
from config import config

ranks = plunder.get_player_ranks()
planet.planets = home.get_planets()
plunder.plunder_galaxy(planet.planets[1], ranks, 800, 6, 1, 499, 45)
