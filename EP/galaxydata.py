import http_requester as requests
from bs4 import BeautifulSoup
from config import config, headers, cookies
import time


def get_asteroid(referer_url, x, y):
    response = get_galaxy_data(x, y, referer_url)

    soup = BeautifulSoup(response.text, "html.parser")
    asteroid_link = soup.find("a", class_="btn-asteroid")

    if not asteroid_link:
        return None, None
    
    time_left = asteroid_link.find("span", {"data-asteroid-disappear": True}).text

    return time_left, response.url


def get_plunder_ids(base_planet_id, x, y, players_rank, minimum_rank, referer_url):
    response = get_galaxy_data(x, y, referer_url, base_planet_id)
    
    soup = BeautifulSoup(response.text, "html.parser")
    inactive_players = soup.find_all("div", class_="galaxy-item filterInactive")

    plunder_ids = []
    for player in inactive_players:
        player_name_tag = player.find("span", class_="text-area isInactive28 tooltip_sticky")
        if player_name_tag == None:
            continue
        player_name = player_name_tag.text

        player_rank = players_rank.get(player_name, 999999)

        if player_rank < minimum_rank:
            id_wrapper = player.find("a", class_="btnActionPlunder tooltip").get("onclick")
            id = id_wrapper.split('\'')[1]
            plunder_ids.append(id)

    return plunder_ids, response.url


def send_plunder(plunder_id, referer_url):
    url = f"{config.server.host}/galaxy/sendplunder"
    headers_dict = {**headers, "referer": referer_url}

    data = {
        "Id": plunder_id
    }

    response = requests.post(url, headers=headers_dict, cookies=cookies, json=data)

    return


def get_galaxy_data(x, y, referer_site, base_planet_id):
    url = f"{config.server.host}/galaxy/galaxydata"
    headers_dict = {**headers, "referer": referer_site}

    params = {
        "x": x,
        "y": y,
        "_": int(time.time() * 1000),
        "planet": base_planet_id
    }

    response = requests.get(url, headers=headers_dict, cookies=cookies, params=params)

    return response
