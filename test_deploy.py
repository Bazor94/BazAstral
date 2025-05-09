from models import models
from services import colonize_planet
from EP import home
from EP import login
from EP import building
import threading
from services import send_expedition
from config import config


models.planets = home.get_planets()
exp_planets = [p for p in models.planets if p.coords in config.crons.expedition.planets]
base_planet = models.search_for_planet(models.planets, "3:147:8")

send_expedition.deploy_split_ships(exp_planets, base_planet)
