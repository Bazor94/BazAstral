from config import config, headers, cookies
import http_requester as requests
import time
from bs4 import BeautifulSoup
from models import models


def increase_building(planet, building, referer_url):
    url = f"{config.server.host}/building/increasebuilding"
    headers_dict = {**headers, "referer": referer_url }

    data = {
        "__PlanetId": planet.id,
        "BuildingType": building
    }

    response = requests.post(url, headers=headers_dict, cookies=cookies, json=data)

    return response.url


def get_buildings_and_resources(planet):
    url = f"{config.server.host}/building/resource"
    headers_dict = {**headers, "referer": f'{config.server.host}/home' }

    params = {
        "planet": planet.id
    }

    response = requests.get(url, headers=headers_dict, cookies=cookies, params=params)

    soup = BeautifulSoup(response.text, "html.parser")

    building_levels = soup.find_all("span", class_="building-level")
    metal_mine = int(building_levels[0].text)
    crystal_mine = int(building_levels[1].text)
    deuterium_refinery = int(building_levels[2].text)

    first_construction_div = soup.find("div", id="firstConstruction")
    if first_construction_div is not None:
        spans = first_construction_div.find_all("span")
        name = spans[0].text
        if name == "Metal Mine":
            metal_mine += 1
        elif name == "Crystal Mine":
            crystal_mine +=1
        elif name == "Deuterium Refinery":
            deuterium_refinery +=1

    construction_queue = soup.find_all("a", class_="construction-queue-item")

    for item in construction_queue:
        building_type = item.get('data-building-type')
        if building_type == "METAL_MINE":
            metal_mine += 1
        elif building_type == "CRYSTAL_MINE":
            crystal_mine +=1
        elif building_type == "DEUTERIUM_REFINERY":
            deuterium_refinery +=1

    buildings = models.Buildings(metal_mine, crystal_mine, deuterium_refinery)

    metal = int(soup.find("span", id="metal-amount").text.replace(".", ""))
    crystal = int(soup.find("span", id="crystal-amount").text.replace(".", ""))
    deuterium = int(soup.find("span", id="deuterium-amount").text.replace(".", ""))
    resources = models.Resources(metal, crystal, deuterium)

    return buildings, resources, response.url

def demolish_building(planet, building):
    url = f"{config.server.host}/building/demolishbuilding"
    headers_dict = {**headers, "referer": f'{config.server.host}/home' }

    data = {
        "__PlanetId": planet.id,
        "BuildingType": building
    }

    response = requests.post(url, headers=headers_dict, cookies=cookies, json=data)

    return response.url