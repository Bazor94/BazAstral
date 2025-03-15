import http_requester as requests
from bs4 import BeautifulSoup
import config
import time

def parse_asteroid(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    asteroid_link = soup.find("a", class_="btn-asteroid")

    if not asteroid_link:
        return False, None, None
    
    asteroid_url = asteroid_link.get("href")
    asteroid_time = asteroid_link.find("span", {"data-asteroid-disappear": True}).text

    return True, asteroid_url, asteroid_time

def get_asteroid(referer_site, x, y):
    url = f"{config.host}/galaxy/galaxydata"
    headers = {**config.headers, "referer": referer_site}

    params = {
        "x": x,
        "y": y,
        "_": int(time.time() * 1000)
    }

    response = requests.get(url, headers=config.headers, cookies=config.cookies, params=params)
    is_asteroid, asteroid_url, time_left = parse_asteroid(response.text)

    return is_asteroid, asteroid_url, time_left, response.url
