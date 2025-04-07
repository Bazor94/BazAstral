import services.build_defense as defense_service
from logger import logger
import threads
from config import config


def build_def_cron(planet):
    threads.stop_threads.wait(7*60)
    build_def(planet)
        

@threads.stoper(threads.stop_threads, threads.running_threads['defense'])
def build_def(planet):
    defense_service.build_max_defense_one_planet(planet)
    logger.sleep_log("defense", planet, config.crons.defense.interval)
    threads.stop_threads.wait(config.crons.defense.interval)