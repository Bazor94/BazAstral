from services import fleet as fleet_service
from EP import planet as planet_ep
from models import planet
from EP import home
import time
from datetime import datetime, timedelta
from logger import logger
import helpers


def colonize_planet(base_coords, coords, min_space, mission_num):
    planet.planets = home.get_planets()
    target_planet = planet.search_for_planet(planet.planets, coords)
    base_planet = planet.search_for_planet(planet.planets, base_coords)

    if target_planet is not None:
        referer_url = planet_ep.get_abandon_planet(target_planet)
        planet_ep.abandon_planet(target_planet, referer_url)


    x, y, z = map(int, coords.split(':'))
    for i in range (0, mission_num):
        logger.info(f'sending colonization mission', extra={"action": "colonize"})
        fleet_service.colonize_planet(x, y, z, base_planet.id)
        time.sleep(10)

    missions = fleet_service.get_missions()['Colonize']
    time_sleep = int((missions[0].arrive_date - datetime.now()).total_seconds()) + 1

    logger.info(f'initial sleeping for  {helpers.format_seconds(time_sleep)}. Till {datetime.now() +timedelta(seconds=time_sleep)}', extra={"action": "colonize"})
    time.sleep(time_sleep)

    for i in range (0, mission_num):
        planet.planets = home.get_planets()
        target_planet = planet.search_for_planet(planet.planets, coords)

        if target_planet is not None:
            fields = home.get_fields(target_planet)
            if int(fields) < int(min_space):
                logger.info(f'deleting a planet with {fields} fields', extra={"action": "colonize"})
                referer_url = planet_ep.get_abandon_planet(target_planet)
                planet_ep.abandon_planet(target_planet, referer_url)
        else:
            pass

        missions = fleet_service.get_missions()['Colonize']
        if len(missions) == 0:
            return
        
        time_sleep = int((missions[0].arrive_date - datetime.now()).total_seconds()) + 1

        logger.info(f'sleeping for  {helpers.format_seconds(time_sleep)}. Till {datetime.now() +timedelta(seconds=time_sleep)}', extra={"action": "colonize"})
        time.sleep(time_sleep)
    
    