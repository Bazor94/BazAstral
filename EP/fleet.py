import requests
from bs4 import BeautifulSoup
import config
import time

ep = '/fleet'
fleet2ep = '/fleet/fleetpage2data'
fleet3ep = '/fleet/fleetpage3data'

def get_fleet_html():
    url = f"{config.host}{ep}"
    headers = {**config.headers, "referer": f"{config.host}/home" }

    response = requests.get(url, headers=config.headers, cookies=config.cookies)

    if response.status_code != 200:
        raise ValueError("get_fleet_html status code is not 200")

    return response.text, response.url

def get_miners_num(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    miners_num = soup.find("a", {"data-ship-type": "ASTEROID_MINER"}).find("span", class_="ship-quantity").text

    return miners_num

def send_fleet_2(miners_num):
    url = f"{config.host}{fleet2ep}"
    headers = {**config.headers, "referer": f"{config.host}/fleet" }

    data = {
        "Ships": [
            {
                "ShipType": "ASTEROID_MINER",
                "Quantity": f"{miners_num}"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise ValueError("send_fleet_2 status code is not 200")

    return response.text


def send_fleet_3(miners_num, x, y, z):
    url = f"{config.host}{fleet3ep}"
    headers = {**config.headers, "referer": f"{config.host}/fleet" }

    data = {
        "TargetX": x,
        "TargetY": y,
        "TargetZ": z,
        "TargetPlanetType": 1,
        "SpeedPercentage": 100,
        "Ships": [
            {
                "ShipType": "ASTEROID_MINER",
                "Quantity": f"{miners_num}"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise ValueError("send_fleet_2 status code is not 200")
    
    print(response.text)
