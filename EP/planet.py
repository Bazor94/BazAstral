from config import config, headers, cookies
import http_requester as requests
import time


def get_abandon_planet(planet):
    url = f"{config.server.host}/home/abandonplanet"
    headers_dict = {**headers, "referer": f"{config.server.host}/home?planet={planet.id}" }

    params = {"planet": planet.id, "_": int(time.time() * 1000)}

    response = requests.get(url, headers=headers_dict, cookies=cookies, params=params)

    return response.url


def abandon_planet(planet, referer_url):
    url = f"{config.server.host}/home/abandonplanet"
    headers_dict = {**headers, "referer": referer_url }

    data = {
        "PlanetId": planet.id,
        "Password": config.password,
        "CoordsX": planet.x,
        "CoordsY": planet.y,
        "CoordsZ": planet.z
    }

    response = requests.post(url, headers=headers_dict, cookies=cookies, json=data)

    return response.url
