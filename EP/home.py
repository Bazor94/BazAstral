import http_requester as requests
from config import config, headers, cookies
from bs4 import BeautifulSoup
import models.models as planet
import threads


def home():
    url = f"{config.server.host}/home"
    headers_dict = {**headers}

    response = requests.get(url, headers=headers_dict, cookies=cookies)

    return response.text


def get_fields(planet):
    url = f"{config.server.host}/home"
    headers_dict = {**headers}

    params = {"planet": planet.id}

    response = requests.get(url, headers=headers_dict, cookies=cookies, params=params)

    soup = BeautifulSoup(response.text, 'html.parser')

    span = soup.find('span', class_='prop-text')
    value = span.find_all('b')[1].text

    return value


@threads.locker(threads.is_idle)
def get_planets():
    html = home()
    soup = BeautifulSoup(html, 'html.parser')

    # Znajdujemy wszystkie planety i ich moony w obrębie `.planet-item`
    planets = []

    for planet_item in soup.select('.planet-item'):
        planet_tag = planet_item.select_one('.planet-select')
        moon_tag = planet_item.select_one('.moon-select')
        name_tag = planet_item.select_one('.planet-name')
        coords_tag = planet_item.select_one('.planet-coords')

        planet_id = planet_tag['href'].split('=')[-1]
        moon_id = moon_tag['href'].split('=')[-1] if moon_tag else None
        planet_name = name_tag.text.strip()
        coords_text = coords_tag.text.strip().strip("[]")
        x, y, z = map(int, coords_text.split(':'))
        p = planet.Planet(coords_text, x, y, z, planet_name, planet_id, moon_id)
        planets.append(p)

    planet.planets = planets
    return planets
