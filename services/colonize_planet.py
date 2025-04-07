from services import fleet_service as fleet_service
from EP import planet as planet_ep
from models import models
from EP import home
import time
from datetime import datetime, timedelta, timezone
from logger import logger
import helpers
import threads


def colonize_planet(base_planet, coords, min_space, mission_num, delete_initial_planet=True):
    if delete_initial_planet:
        delete_planet(base_planet, coords, min_space)

    x, y, z = map(int, coords.split(':'))
    for i in range (0, mission_num):
        logger.info(f'{coords} | sending colonization mission', extra={"planet": base_planet, "action": "colonize"})
        fleet_service.colonize_planet(x, y, z, base_planet.id)
        time.sleep(10)

    missions = get_missions_from_coords(coords)
    if len(missions) == 0:
        logger.error(f'{coords} | there are no colonize missions', extra={"planet": base_planet, "action": "colonize"})
        return
    
    time_sleep = int((missions[0].arrive_date - datetime.now()).total_seconds()) + 3
    logger.sleep_log("colonize", base_planet, time_sleep, prefix=f'{coords} | initial')
    time.sleep(time_sleep)

    mission_num = len(missions)
    while mission_num > 0:
        is_deleted = delete_planet(base_planet, coords, min_space)
        if is_deleted == False:
            return

        missions = get_missions_from_coords(coords)
        mission_num = len(missions)
        if mission_num == 0:
            return
        
        if missions[0].arrive_date > datetime.now():
            time_sleep = int((missions[0].arrive_date - datetime.now()).total_seconds()) + 1
            logger.sleep_log("colonize", base_planet, time_sleep, prefix=f'{coords} |')
            time.sleep(time_sleep)
        

def get_missions_from_coords(coords):
    missions = fleet_service.get_missions()['Colonize']
    planet_missions = [m for m in missions if m.target_coords == coords]

    return planet_missions


@threads.locker()
def delete_planet(base_planet, coords, min_space):
    planets = home.get_planets()
    target_planet = models.search_for_planet(planets, coords)

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
        
    