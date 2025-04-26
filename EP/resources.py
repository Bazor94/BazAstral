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

    metal = int(soup.find("span", id="metal-amount").text.replace(".", ""))
    crystal = int(soup.find("span", id="crystal-amount").text.replace(".", ""))
    deuterium = int(soup.find("span", id="deuterium-amount").text.replace(".", ""))

    return models.Resources(metal, crystal, deuterium), response.url

def demolish_building(planet, building):
    url = f"{config.server.host}/building/demolishbuilding"
    headers_dict = {**headers, "referer": f'{config.server.host}/home' }

    data = {
        "__PlanetId": planet.id,
        "BuildingType": building
    }

    response = requests.post(url, headers=headers_dict, cookies=cookies, json=data)

    return response.url