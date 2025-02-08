import requests
import config

ep = '/galaxy'

def get_galaxy_html():
    url = f"{config.host}{ep}"
    headers = {**config.headers, "referer": "https://lyra.ogamex.net/home"}
    
    response = requests.get(url, headers=config.headers, cookies=config.cookies)

    if response.status_code != 200:
        raise ValueError("get_galaxy_html status code is not 200")

    return response.text

def get_current_coord():
    return

