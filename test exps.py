from config import config
import EP.login as login
from EP import home
import threading
import time
from models import models
import threads
from crons import asteroid, expedition, plunder, refresh, collect, defense, bonus
from services import build_defense, send_expedition

#login.login()
models.planets = home.get_planets()
exp_planets = send_expedition.get_planets_from_coords(config.crons.expedition.planets)
main_planet = models.search_for_planet(models.planets, config.crons.expedition.planets[0])
t = threading.Thread(target=expedition.send_expedition_cron, args=(exp_planets,))
t.start()
t.join()
