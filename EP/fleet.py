import http_requester as requests
from bs4 import BeautifulSoup
import config
import time
from datetime import datetime
from models import planet

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


def submit_fleet(ships, x, y, z, mission_type, target_planet, referer_url, speed=100):
    url = f"{config.host}/fleet/submitfleet"
    headers = {**config.headers, "referer": referer_url }

    data = {
        "TargetX": x,
        "TargetY": y,
        "TargetZ": z,
        "TargetPlanetType": 1,
        "SpeedPercentage": speed,
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

    updated_ships = {"Ships": []}
    for ship in ships['Ships']:
        if ship['ShipType'] in ['LIGHT_CARGO', 'ASTEROID_MINER']:
            continue
        updated_ships['Ships'].append({'ShipType': ship['ShipType'], 'Quantity': str(ship['Quantity'])})

    data.update(updated_ships)

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
        mission = fleet.find("span", class_="mission-left").text.strip()
        date_left = fleet.find("span", class_="date-left")
        date_right = fleet.find("span", class_="date-right")
        coords_from = fleet.select_one('.fromPlanet a').text[1:-1]
        coords_to = fleet.select_one('.toPlanet a').text[1:-1]

        if date_right == None: # fleet is returning
            arrive_date = None
            back_date = datetime.strptime(date_left.text.strip(), "%d.%m.%Y %H:%M:%S")
        elif mission == 'Transport': # transport is a little bit fucked up
            start_date = datetime.strptime(date_left.text.strip(), "%d.%m.%Y %H:%M:%S")
            arrive_date = datetime.strptime(date_right.text.strip(), "%d.%m.%Y %H:%M:%S")
            back_date = start_date + 2 * (arrive_date - start_date)
        else:
            arrive_date = datetime.strptime(date_left.text.strip(), "%d.%m.%Y %H:%M:%S")
            back_date = datetime.strptime(date_right.text.strip(), "%d.%m.%Y %H:%M:%S")

        missions.append(Mission(arrive_date, back_date, mission, coords_from, coords_to))

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
    def __init__(self, arrive_date, back_date, mission_type: str, coords_from: str, coords_to: str):
        self.arrive_date = arrive_date
        self.back_date = back_date
        self.planet = planet.search_for_planet(planet.planets, coords_from)
        self.target_coords = coords_to

        self.type = mission_type
