import requests
import config

ep = '/defense'
ep2 = '/defense/createdefense'

def defense(planet_id):
    url = f"{config.host}{ep}"
    headers = {**config.headers, "referer": f"{config.host}/home" }

    params = {
        "planet": planet_id
    }

    response = requests.post(url, headers=headers, params=params)

    if response.status_code != 200:
        raise ValueError("defense status code is not 200")

    return response.text

def create_defense(planet_id):
    url = f"{config.host}{ep}"
    headers = {**config.headers, "referer": f"{config.host}/defense" }

    params = {
        "planet": planet_id
    }

    response = requests.post(url, headers=headers, json=data, params=params)

    if response.status_code != 200:
        raise ValueError("defense status code is not 200")

    return response.text