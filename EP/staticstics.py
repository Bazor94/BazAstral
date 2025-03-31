from config import config, headers, cookies
import http_requester as requests
from bs4 import BeautifulSoup
import time

def get_players_ranks(page, referer_url=f"{config.server.host}/home"):
    url = f"{config.server.host}/statistics/statisticsdata"
    headers_dict = {**headers, "referer": referer_url }

    params = {
        "Category": "PLAYER",
        "SubCategory": "POINTS",
        "Page": page,
        "Rel": "",
        "_": int(time.time() * 1000)
    }   

    response = requests.get(url, headers=headers_dict, cookies=cookies, params=params)

    soup = BeautifulSoup(response.text, 'html.parser')
    table_container = soup.find("div", class_="statistics-table-container")
    body = table_container.find("tbody")

    tr_elements = body.find_all("tr")

    stats = {}
    for tr in tr_elements:
        place = int(tr.find("td").text)
        links = tr.find_all("a")

        if len(links) == 3:
            name = links[1].text
        elif len(links) == 2:
            name = links[0].text 

        stats[name] = place

    return stats, response.url



        