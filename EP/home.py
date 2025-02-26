import requests
import config
from bs4 import BeautifulSoup

ep = '/home'

def home():
    url = f"{config.host}{ep}"
    headers = {**config.headers}

    response = requests.get(url, headers=headers, cookies=config.cookies)

    if response.status_code != 200:
        raise ValueError("home status code is not 200")

    return response.text

def get_planet_ids():
    html = home()
    print(html)

    soup = BeautifulSoup(html, 'html.parser')

    # Znajdujemy wszystkie planety i ich moony w obrębie `.planet-item`
    planet_moon_pairs = []

    for planet_item in soup.select('.planet-item'):
        planet_tag = planet_item.select_one('.planet-select')
        moon_tag = planet_item.select_one('.moon-select')

        if planet_tag:
            planet_id = planet_tag['href'].split('=')[-1]
            moon_id = moon_tag['href'].split('=')[-1] if moon_tag else None
            planet_moon_pairs.append((planet_id, moon_id))

    return planet_moon_pairs