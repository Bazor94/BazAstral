import http_requester as requests
from bs4 import BeautifulSoup
import config
import time
from datetime import datetime

def get_fleet(planet_id):
    url = f"{config.host}/fleet"
    headers = {**config.headers, "referer": f"{config.host}/home" }
    params = {"planet": planet_id}

    response = requests.get(url, headers=headers, cookies=config.cookies, params=params)

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


def send_fleet_2(ships, referer_url):
    url = f"{config.host}/fleet/fleetpage2data"
    headers = {**config.headers, "referer": referer_url }

    data = {}
    data.update(ships)
    response = requests.post(url, headers=headers, cookies=config.cookies, json=data)

    return response.text


def send_fleet_3(ships, x, y, z, referer_url):
    url = f"{config.host}/fleet/fleetpage3data"
    headers = {**config.headers, "referer": referer_url }

    data = {
        "TargetX": x,
        "TargetY": y,
        "TargetZ": z,
        "TargetPlanetType": 1,
        "SpeedPercentage": 100,
    }
    data.update(ships)

    requests.post(url, headers=headers, cookies=config.cookies, json=data)


def submit_fleet(ships, x, y, z, mission_type, target_planet, referer_url):
    url = f"{config.host}/fleet/submitfleet"
    headers = {**config.headers, "referer": referer_url }

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

    requests.post(url, headers=headers, cookies=config.cookies, json=data)
    

def get_autoexpedition_fleet(planet_id, referer_url):
    url = f"{config.host}/fleet/autoexpedition"
    headers = {**config.headers, "referer": referer_url }
    params = {"planet": planet_id}

    response = requests.get(url, headers=headers, cookies=config.cookies, params=params)

    return response.text, response.url

def send_autoexpedition_fleet(ships, exp_count, referer_url):
    url = f"{config.host}/fleet/sendautoexpedition"
    headers = {**config.headers, "referer": referer_url }

    data = {
        "ExpeditionCount": f"{exp_count}",
        "ExpeditionDuration": "40",
        "FleetSpeed": "100"
    }
    data.update(ships)

    response = requests.post(url, headers=headers, cookies=config.cookies, json=data)

    return response.text, response.url

def get_feet_movement():
    url = f"{config.host}/fleet/fleetmovements"
    headers = {**config.headers, "referer": f"{config.host}/fleet" }

    response = requests.get(url, headers=headers, cookies=config.cookies)

    soup = BeautifulSoup(response.text, 'html.parser')

    missions = []

    fleet_items = soup.find_all("div", {"class": "fleet-item"})
    for fleet in fleet_items:
        date_left = fleet.find("span", class_="date-left")
        date_right = fleet.find("span", class_="date-right")
        mission = fleet.find("span", class_="mission-left")

        missions.append(Mission(date_left, date_right, mission.text.strip()))

    return missions, response.url

def get_collect_resources(planet_id, referer_url):
    url = f"{config.host}/fleet/collectresources"
    headers = {**config.headers, "referer": referer_url }
    params = {"planet": planet_id}
    response = requests.get(url, headers=headers, cookies=config.cookies, params=params)

    return response.text, response.url

def collect_all_resources(planet_id, planet_ids, ships, referer_url):
    url = f"{config.host}/fleet/collectallresources"
    headers = {**config.headers, "referer": referer_url }
    params = {"planet": planet_id}
    data = {
        "PlanetIds": planet_ids,
        "Ships": ships
    }

    response = requests.post(url, headers=headers, cookies=config.cookies, params=params, json=data)

    return response.text, response.url

class Mission:
    def __init__(self, date_left: str, date_right: str, mission_type: str):
        self.date_left = datetime.strptime(date_left.text.strip(), "%d.%m.%Y %H:%M:%S") if date_left else None
        self.date_right = datetime.strptime(date_right.text.strip(), "%d.%m.%Y %H:%M:%S") if date_right else None
        self.type = mission_type
