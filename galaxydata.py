import requests
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

    return response.text