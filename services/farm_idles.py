from EP import staticstics
from EP import galaxydata
from config import config
import math
from services import fleet as fleet_service
import threads

time_sleep = 5 * 60

def get_player_ranks(min_rank=1000):
    max_page = math.ceil(min_rank / 100) + 1
    referer_url = f"{config.server.host}/home"

    stats = {}
    for page_num in range (1, max_page):
        page_stats, referer_url = staticstics.get_players_ranks(page_num, referer_url)
        stats.update(page_stats)

    return stats

def plunder_galaxy(base_planet_id, player_ranks, min_rank, x, min_y, max_y, max_plunder_missions): 
    missions = fleet_service.get_missions()['Attack']
    plunder_missions = len(missions)
   
    referer_url = f'{config.server.host}/galaxy?planet={base_planet_id}'
    for y in range (min_y, max_y):
        plunder_ids, referer_url = galaxydata.get_plunder_ids(base_planet_id, x, y, player_ranks, min_rank, referer_url)

        for id in plunder_ids:
            while plunder_missions >= max_plunder_missions:
                threads.stop_threads.wait(time_sleep)
                missions = fleet_service.get_missions()['Attack']
                plunder_missions = len(missions)

            galaxydata.send_plunder(id, referer_url)
            plunder_missions += 1
            
