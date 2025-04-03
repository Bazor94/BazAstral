from EP import staticstics
from EP import galaxydata
from config import config
import math
from services import fleet_service as fleet_service
import threads
from logger import logger
import helpers
from datetime import datetime, timedelta

idle_wait = config.crons.plunder.idle_time

def get_player_ranks(min_rank=1000):
    max_page = math.ceil(min_rank / 100) + 1
    referer_url = f"{config.server.host}/home"

    stats = {}
    for page_num in range (1, max_page):
        page_stats, referer_url = staticstics.get_players_ranks(page_num, referer_url)
        stats.update(page_stats)

    return stats

def plunder_galaxy(base_planet, player_ranks, min_rank, x, min_y, max_y, max_plunder_missions): 
    missions = get_plunder_mission_per_planet(base_planet)
    plunder_missions = len(missions)
   
    referer_url = f'{config.server.host}/galaxy?planet={base_planet.id}'
    for y in range (min_y, max_y):
        plunder_ids, referer_url = galaxydata.get_plunder_ids(base_planet.id, x, y, player_ranks, min_rank, referer_url)

        for id in plunder_ids:
            while plunder_missions >= max_plunder_missions:
                logger.info(f'idle sleeping for {helpers.format_seconds(idle_wait)}. Till {datetime.now() + timedelta(seconds=idle_wait)}', extra={"planet": base_planet, "action": "plunder"})
                threads.stop_threads.wait(idle_wait)
                missions = get_plunder_mission_per_planet(base_planet)
                plunder_missions = len(missions)

            if threads.stop_threads.is_set() or not threads.running_threads['plunder'].is_set():
                return

            try:
                galaxydata.send_plunder(id, base_planet.id, referer_url)
            except Exception as e:
                logger.warning(e)

            plunder_missions += 1
            
def get_plunder_mission_per_planet(planet):
    missions = fleet_service.get_missions()['Attack']
    planet_mission = [m for m in missions if m.planet == planet]

    return planet_mission