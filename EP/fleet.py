import http_requester as requests
from bs4 import BeautifulSoup
from config import config, headers, cookies
import time
from datetime import datetime
from models import mission
import json

def get_fleet(planet_id):
    url = f"{config.server.host}/fleet"
    headers_dict = {**headers, "referer": f"{config.server.host}/home" }
    params = {"planet": planet_id}

    response = requests.get(url, headers=headers_dict, cookies=cookies, params=params)

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
    url = f"{config.server.host}/fleet/fleetpage2data"
    headers_dict = {**headers, "referer": referer_url }

    data = {}
    data.update(ships)
    response = requests.post(url, headers=headers_dict, cookies=cookies, json=data)

    return response.text


def send_fleet_3(ships, x, y, z, referer_url):
    url = f"{config.server.host}/fleet/fleetpage3data"
    headers_dict = {**headers, "referer": referer_url }

    data = {
        "TargetX": x,
        "TargetY": y,
        "TargetZ": z,
        "TargetPlanetType": 1,
        "SpeedPercentage": 100,
    }
    data.update(ships)

    resp = requests.post(url, headers=headers_dict, cookies=cookies, json=data)

    try:
        response_dict = json.loads(resp)
    except:
        return None
    
    return response_dict


def submit_fleet(ships, x, y, z, mission_type, target_planet, referer_url, speed=100):
    url = f"{config.server.host}/fleet/submitfleet"
    headers_dict = {**headers, "referer": referer_url }

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

    resp = requests.post(url, headers=headers_dict, cookies=cookies, json=data)
    return


def get_autoexpedition_fleet(planet_id, referer_url):
    url = f"{config.server.host}/fleet/autoexpedition"
    headers_dict = {**headers, "referer": referer_url }
    params = {"planet": planet_id}

    response = requests.get(url, headers=headers_dict, cookies=cookies, params=params)

    return response.text, response.url

def send_autoexpedition_fleet(ships, exp_count, referer_url):
    url = f"{config.server.host}/fleet/sendautoexpedition"
    headers_dict = {**headers, "referer": referer_url }

    data = {
        "ExpeditionCount": f"{exp_count}",
        "ExpeditionDuration": "60",
        "FleetSpeed": "100"
    }

    updated_ships = {"Ships": []}
    for ship in ships['Ships']:
        if ship['ShipType'] in ['ASTEROID_MINER']:
            continue
        updated_ships['Ships'].append({'ShipType': ship['ShipType'], 'Quantity': str(ship['Quantity'])})

    data.update(updated_ships)

    response = requests.post(url, headers=headers_dict, cookies=cookies, json=data)

    return response.text, response.url

def get_feet_movement():
    url = f"{config.server.host}/fleet/fleetmovements"
    headers_dict = {**headers, "referer": f"{config.server.host}/fleet" }

    response = requests.get(url, headers=headers_dict, cookies=cookies)

    soup = BeautifulSoup(response.text, 'html.parser')

    missions = []

    fleet_items = soup.find_all("div", {"class": "fleet-item"})
    for fleet in fleet_items:
        mission_type = fleet.find("span", class_="mission-left").text.strip()
        date_left = fleet.find("span", class_="date-left")
        date_right = fleet.find("span", class_="date-right")
        coords_from = fleet.select_one('.fromPlanet a').text[1:-1]
        coords_to = fleet.select_one('.toPlanet a').text[1:-1]

        if date_right == None: # fleet is returning
            arrive_date = None
            back_date = datetime.strptime(date_left.text.strip(), "%d.%m.%Y %H:%M:%S")
        elif mission_type == 'Transport': # transport is a little bit fucked up
            start_date = datetime.strptime(date_left.text.strip(), "%d.%m.%Y %H:%M:%S")
            arrive_date = datetime.strptime(date_right.text.strip(), "%d.%m.%Y %H:%M:%S")
            back_date = start_date + 2 * (arrive_date - start_date)
        else:
            arrive_date = datetime.strptime(date_left.text.strip(), "%d.%m.%Y %H:%M:%S")
            back_date = datetime.strptime(date_right.text.strip(), "%d.%m.%Y %H:%M:%S")

        missions.append(mission.Mission(arrive_date, back_date, mission_type, coords_from, coords_to))

    return missions, response.url

def get_collect_resources(planet_id, referer_url):
    url = f"{config.server.host}/fleet/collectresources"
    headers_dict = {**headers, "referer": referer_url }
    params = {"planet": planet_id}
    response = requests.get(url, headers=headers_dict, cookies=cookies, params=params)

    return response.text, response.url

def collect_all_resources(planet_id, planet_ids, ships, referer_url):
    url = f"{config.server.host}/fleet/collectallresources"
    headers_dict = {**headers, "referer": referer_url }
    params = {"planet": planet_id}
    data = {
        "PlanetIds": planet_ids,
        "Ships": ships
    }

    response = requests.post(url, headers=headers_dict, cookies=cookies, params=params, json=data)

    return response.text, response.url
