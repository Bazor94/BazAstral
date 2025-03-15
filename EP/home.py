import requests
import config
from bs4 import BeautifulSoup
import models.planet as planet

ep = '/home'

def home():
    url = f"{config.host}{ep}"
    headers = {**config.headers}

    response = requests.get(url, headers=headers, cookies=config.cookies)

    if response.status_code != 200:
        raise ValueError("home status code is not 200")

    return response.text

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
        p = planet.Planet(x, y, z, planet_name, planet_id, moon_id)
        planets.append(p)

    return planets