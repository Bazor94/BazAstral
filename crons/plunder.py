import threading
from config import config
import threads
from services import plunder
from EP import home
from models import planet
import math
 

@threads.stoper(threads.stop_threads, threads.running_threads['plunder'])
def plunder_single_planet(base_planet, player_ranks, min_rank, x, min_y, max_y, max_plunder_missions):
    plunder.plunder_galaxy(base_planet, player_ranks, min_rank, x, min_y, max_y, max_plunder_missions)


def plunder_cron():
    ranks = plunder.get_player_ranks()
    planet.planets = home.get_planets()
    max_mission_per_planet = math.floor(config.crons.plunder.max_missions / len(config.crons.plunder.planets))
    
    threads = []
    for planet_config in config.crons.plunder.planets:
        base_planet = planet.search_for_planet(planet.planets, planet_config.base_coords)
        min_y, max_y = planet_config.y_limit.split(":")

        thread = threading.Thread(target=plunder_single_planet, args=(base_planet, ranks, config.crons.plunder.min_rank, base_planet.x, int(min_y), int(max_y), max_mission_per_planet))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
