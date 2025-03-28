from config import config, headers, cookies
import http_requester as requests
from bs4 import BeautifulSoup

class Resources:
    def __init__(self, metal, crystal, deuterium):
        self.metal = metal
        self.crystal = crystal
        self.deuterium = deuterium

class PlanetEmpire:
    def __init__(self, planet):
        self.planet = planet
    
    def set_resources(self, resources: Resources):
        self.resources = resources

    def set_moon_resources(self, resources: Resources):
        self.moon_resources = resources


class Empire:
    def __init__(self, planet_empires):
        self.planet_empires = planet_empires


def str2int(resource_str):
    return int(resource_str.replace('.',''))


def get_empire_info(planets):
    url = f"{config.server.host}/empire"
    headers_dict = {**headers, "referer": f"{config.server.host}/home" }

    response = requests.get(url, headers=headers_dict, cookies=cookies)

    soup = BeautifulSoup(response.text, 'html.parser')

    planet_view_container = soup.find('div', class_='planetViewContainer')
    rows = planet_view_container.find_all('div', class_='prop-row')
    resources = rows[0]

    empire = {}
    for p in planets:
        empire[p.coords] = {}

    for col, planet in zip(resources.find_all('div', class_='col')[1:], planets):
        res_list = col.find_all('span', class_='cell-value')
        metal = str2int(res_list[0].text)
        crystal = str2int(res_list[0].text)
        deuterium = str2int(res_list[0].text)
        empire[planet.coords]["resources"] = Resources(metal, crystal, deuterium)
    
    moon_view_container = soup.find('div', class_='moonViewContainer')
    rows = moon_view_container.find_all('div', class_='prop-row')
    resources = rows[0]
    for col, planet in zip(resources.find_all('div', class_='col')[1:], planets):
        res_list = col.find_all('span', class_='cell-value')
        metal = str2int(res_list[0].text)
        crystal = str2int(res_list[0].text)
        deuterium = str2int(res_list[0].text)
        empire[planet.coords]["moon_resources"] = Resources(metal, crystal, deuterium)

    return empire