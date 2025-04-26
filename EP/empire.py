from config import config, headers, cookies
import http_requester as requests
from bs4 import BeautifulSoup
from models import models


def str2int(resource_str):
    return int(resource_str.replace('.',''))


class Buildings:
    def __init__(self, metal, crystal, deuterium):
        self.metal = metal
        self.crystal = crystal
        self.deuterium = deuterium
    


def get_empire_info(planets):
    url = f"{config.server.host}/empire"
    headers_dict = {**headers, "referer": f"{config.server.host}/home" }

    response = requests.get(url, headers=headers_dict, cookies=cookies)

    soup = BeautifulSoup(response.text, 'html.parser')

    planet_view_container = soup.find('div', class_='planetViewContainer')
    rows = planet_view_container.find_all('div', class_='prop-row')
    
    empire = {}
    for p in planets:
        empire[p.coords] = {}

    resources = rows[0]
    for col, planet in zip(resources.find_all('div', class_='col')[2:], planets):
        res_list = col.find_all('span', class_='cell-value')
        metal = str2int(res_list[0].text)
        crystal = str2int(res_list[1].text)
        deuterium = str2int(res_list[2].text)
        empire[planet.coords]["resources"] = models.Resources(metal, crystal, deuterium)
    
    moon_view_container = soup.find('div', class_='moonViewContainer')
    moon_rows = moon_view_container.find_all('div', class_='prop-row')
    resources = moon_rows[0]
    for col, planet in zip(resources.find_all('div', class_='col')[2:], planets):
        res_list = col.find_all('span', class_='cell-value')
        metal = str2int(res_list[0].text)
        crystal = str2int(res_list[1].text)
        deuterium = str2int(res_list[2].text)
        empire[planet.coords]["moon_resources"] = models.Resources(metal, crystal, deuterium)


    production = rows[1]
    for col, planet in zip(production.find_all('div', class_='col')[2:], planets):
        res_list = col.find_all('span', class_='cell-value')
        metal = str2int(res_list[0].text)
        crystal = str2int(res_list[1].text)
        deuterium = str2int(res_list[2].text)
        empire[planet.coords]["production"] = models.Resources(metal, crystal, deuterium)


    building = rows[3]
    for col, planet in zip(building.find_all('div', class_='col')[2:], planets):
        res_list = col.find_all('span', class_='cell-value')
        metal = int(res_list[0].text)
        crystal = int(res_list[1].text)
        deuterium = int(res_list[2].text)
        empire[planet.coords]["buildings"] = models.Buildings(metal, crystal, deuterium)
    

    return empire