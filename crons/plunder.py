import threading
from config import config
import models.models
import threads
from services import plunder
from EP import home
import math
import time
 

@threads.stoper(threads.stop_threads, threads.running_threads['plunder'])
def plunder_single_planet(base_planet, player_ranks, min_rank, x, min_y, max_y, max_plunder_missions):
    plunder.plunder_galaxy(base_planet, player_ranks, min_rank, x, min_y, max_y, max_plunder_missions)


def plunder_cron():
    time.sleep(60*3)
    ranks = plunder.get_player_ranks()
    models.models.planets = home.get_planets()
    
    threads = []
    for planet_config in config.crons.plunder.planets:
        base_planet = models.models.search_for_planet(models.models.planets, planet_config.base_coords)
        min_y, max_y = planet_config.y_limit.split(":")

        thread = threading.Thread(target=plunder_single_planet, args=(base_planet, ranks, config.crons.plunder.min_rank, base_planet.x, int(min_y), int(max_y), planet_config.max_missions))
        threads.append(thread)
        thread.start()
        time.sleep(60)

    for thread in threads:
        thread.join()
