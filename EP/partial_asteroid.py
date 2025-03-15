import http_requester as requests
from bs4 import BeautifulSoup
import config
import time


def get_asteroid_locations(referer_site):
    url = f"{config.host}/galaxy/Partial_AsteroidLocation"
    headers = {**config.headers, "referer": referer_site}

    params = {
        "_": int(time.time() * 1000)
    }

    response = requests.get(url, headers=config.headers, cookies=config.cookies, params=params)

    soup = BeautifulSoup(response.text, "html.parser")

    coords = []
    table = soup.find("table", {"id": "playerAsteroidTable"})
    if table is None:
        return coords
    
    for row in table.find_all("tr"):
        links = row.find_all("a")
        if len(links) == 2:
            first = links[0].text.strip().strip("[]").split(":")
            second = links[1].text.strip().strip("[]").split(":")
            coords.append((int(first[1]), int(second[1])))

    return coords