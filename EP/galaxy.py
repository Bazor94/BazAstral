import http_requester as requests
import config

def get_galaxy_html():
    url = f"{config.host}/galaxy"
    headers = {**config.headers, "referer": f"{config.host}/home"}
    
    response = requests.get(url, headers=config.headers, cookies=config.cookies)

    return response.text, response.url

