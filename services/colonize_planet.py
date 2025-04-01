from services import fleet as fleet_service
from EP import planet as planet_ep
from models import planet
from EP import home
import time
from datetime import datetime, timedelta, timezone
from logger import logger
import helpers
import threads


def colonize_planet(base_planet, coords, min_space, mission_num, delete_initial_planet=True):
    if delete_initial_planet:
        delete_planet(coords)

    x, y, z = map(int, coords.split(':'))
    for i in range (0, mission_num):
        logger.info(f'{coords} | sending colonization mission', extra={"planet": base_planet, "action": "colonize"})
        fleet_service.colonize_planet(x, y, z, base_planet.id)
        time.sleep(10)

    missions = fleet_service.get_missions()['Colonize']
    planet_missions = [m for m in missions if m.target_coords == coords]
    if len(planet_missions) == 0:
        logger.error(f'{coords} | there are no colonize missions', extra={"planet": base_planet, "action": "colonize"})
        return
    
    time_sleep = int((planet_missions[0].arrive_date - datetime.now(timezone.utc)).total_seconds()) + 3
    logger.info(f'{coords} | initial sleeping for  {helpers.format_seconds(time_sleep)}. Till {datetime.now() +timedelta(seconds=time_sleep)}', extra={"planet": base_planet, "action": "colonize"})
    time.sleep(time_sleep)

    for i in range (0, mission_num):
        is_deleted = delete_planet(base_planet, coords, min_space)
        if is_deleted == False:
            return

        missions = fleet_service.get_missions()['Colonize']
        planet_missions = [m for m in missions if m.target_coords == coords]
        if len(planet_missions) == 0:
            return
        
        if planet_missions[0].arrive_date > datetime.now(timezone.utc):
            time_sleep = int((planet_missions[0].arrive_date - datetime.now(timezone.utc)).total_seconds()) + 1 + 3600
            logger.info(f'{coords} | sleeping for  {helpers.format_seconds(time_sleep)}. Till {datetime.now() +timedelta(seconds=time_sleep)}', extra={"planet": base_planet, "action": "colonize"})
            time.sleep(time_sleep)
        

def get_missions_from_coords():
    pass


@threads.locker(threads.is_idle)
def delete_planet(base_planet, coords, min_space):
    planets = home.get_planets()
    target_planet = planet.search_for_planet(planets, coords)

    if target_planet is not None:
        fields = home.get_fields(target_planet)
        if int(fields) < int(min_space):
            logger.info(f'{coords} | deleting a planet with {fields} fields', extra={"planet": base_planet, "action": "colonize"})
            referer_url = planet_ep.get_abandon_planet(target_planet)
            planet_ep.abandon_planet(target_planet, referer_url)

            return True
        else:
            logger.info(f'{coords} | saving a planet with {fields} fields', extra={"planet": base_planet, "action": "colonize"})
            return False
        
    