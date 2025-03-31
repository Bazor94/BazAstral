from EP import staticstics
from EP import galaxydata
from config import config
import math

def get_player_ranks(min_rank=1000):
    max_page = math.ceil(min_rank / 100) + 1
    referer_url = f"{config.server.host}/home"

    stats = {}
    for page_num in range (1, max_page):
        page_stats, referer_url = staticstics.get_players_ranks(page_num, referer_url)
        stats = stats | page_stats

    return stats

def plunder_galaxy(player_ranks, min_rank, x, min_y, max_y, max_plunder_missions):
    for y in range (min_y, max_y):
        plunder_ids, referer_url = galaxydata.get_plunder_ids(x, y, player_ranks, min_rank)

        for id in plunder_ids:
            max_plunder_missions += 0
            galaxydata.send_plunder(id, referer_url)

