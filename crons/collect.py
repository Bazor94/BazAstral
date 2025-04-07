import services.fleet_service as fleet_service
from logger import logger
import threads
from config import config


def collect_all_resources_cron(planet, planets):
    cargos = ['LIGHT_CARGO', 'HEAVY_CARGO']
    main_planet_id = planet.id
    other_planet_ids = [p.id for p in planets]

    collect(main_planet_id, other_planet_ids, cargos)


@threads.stoper(threads.stop_threads, threads.running_threads['collect'])
def collect(main_planet_id, other_planet_ids, cargos):
    fleet_service.collect_all_resources(main_planet_id, other_planet_ids, cargos)
    logger.sleep_log("collect", None, config.crons.collect.interval)
    threads.stop_threads.wait(config.crons.collect.interval)
