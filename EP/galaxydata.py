import requests
from bs4 import BeautifulSoup
import config
import time

ep = '/galaxy/galaxydata'

def get_galaxydata_html(referer_site, x, y):
    url = f"{config.host}{ep}"
    headers = {**config.headers, "referer": referer_site}

    params = {
        "x": x,
        "y": y,
        "_": int(time.time() * 1000)
    }

    response = requests.get(url, headers=config.headers, cookies=config.cookies, params=params)

    if response.status_code != 200:
        raise ValueError("get_galaxydata_html status code is not 200")

    return response.text, response.url

def parse_asteroid(raw_html):
    #print(raw_html)

    soup = BeautifulSoup(raw_html, "html.parser")
    asteroid_link = soup.find("a", class_="btn-asteroid")

    if not asteroid_link:
        return False, None, None
    
    asteroid_url = asteroid_link.get("href")
    asteroid_time = asteroid_link.find("span", {"data-asteroid-disappear": True}).text

    return True, asteroid_url, asteroid_time

def get_asteroid(referer_site, x, y):
    raw_html, referal_url = get_galaxydata_html(referer_site, x, y)
    is_asteroid, url, time_left = parse_asteroid(raw_html)

    return is_asteroid, url, time_left, referal_url
