import requests
from bs4 import BeautifulSoup
import config
import time

ep = '/fleet'
fleet2ep = '/fleet/fleetpage2data'
fleet3ep = '/fleet/fleetpage3data'
submit_fleet_ep = '/fleet/submitfleet'

def get_fleet():
    url = f"{config.host}{ep}"
    headers = {**config.headers, "referer": f"{config.host}/home" }

    response = requests.get(url, headers=config.headers, cookies=config.cookies)

    if response.status_code != 200:
        raise ValueError("get_fleet_html status code is not 200")

    return parse_ships(response.text), response.url

def parse_ships(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")

    ships_list = []
    ship_items = soup.find_all("div", class_="ship-item")

    for ship in ship_items:
        ship_type = ship.find("a", class_="ship-btn")["data-ship-type"]
        
        ship_quantity = int(ship.find("a", class_="ship-btn")["data-ship-quantity"])
        
        ships_list.append({
            "ShipType": ship_type,
            "Quantity": ship_quantity
        })

    result = {"Ships": ships_list}
    return result

def send_fleet_2(ships):
    url = f"{config.host}{fleet2ep}"
    headers = {**config.headers, "referer": f"{config.host}/fleet" }

    data = {}
    data.update(ships)
    response = requests.post(url, headers=headers, cookies=config.cookies, json=data)

    if response.status_code != 200:
        raise ValueError("send_fleet_2 status code is not 200")

    return response.text


def send_fleet_3(ships, x, y, z):
    url = f"{config.host}{fleet3ep}"
    headers = {**config.headers, "referer": f"{config.host}/fleet" }

    data = {
        "TargetX": x,
        "TargetY": y,
        "TargetZ": z,
        "TargetPlanetType": 1,
        "SpeedPercentage": 100,
    }
    data.update(ships)

    response = requests.post(url, headers=headers, cookies=config.cookies, json=data)

    if response.status_code != 200:
        raise ValueError("send_fleet_2 status code is not 200")


def submit_fleet(ships, x, y, z, mission_type, target_planet):
    url = f"{config.host}{submit_fleet_ep}"
    headers = {**config.headers, "referer": f"{config.host}/fleet" }

    data = {
        "TargetX": x,
        "TargetY": y,
        "TargetZ": z,
        "TargetPlanetType": 1,
        "SpeedPercentage": 100,
        "MissionType": mission_type,
        "TargetPlanetType": target_planet
    }
    data.update(ships)

    response = requests.post(url, headers=headers, cookies=config.cookies, json=data)

    if response.status_code != 200:
        raise ValueError("submit_fleet status code is not 200")
