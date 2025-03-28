import http_requester as requests
from config import config, headers, cookies

def get_galaxy_html():
    url = f"{config.server.host}/galaxy"
    headers_dict = {**headers, "referer": f"{config.server.host}/home"}
    
    response = requests.get(url, headers=headers_dict, cookies=cookies)

    return response.text, response.url

