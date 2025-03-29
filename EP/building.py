import http_requester as requests
from bs4 import BeautifulSoup
from config import config, headers, cookies
import time
from datetime import datetime
from models import mission
import json


def create_building(planet_id, building, level):
    url = f"{config.server.host}/building/createbuilding"
    headers_dict = {**headers, "referer": f"{config.server.host}/building/resource" }
    data = {
        "BuildingType": building,
        "ToLevel": level,
        "__PlanetId": planet_id
    }

    response = requests.post(url, headers=headers_dict, cookies=cookies, json=data)

    return 