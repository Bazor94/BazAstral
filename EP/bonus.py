import requests
from config import config, headers, cookies
from bs4 import BeautifulSoup
from logger import logger
from datetime import timedelta

providers = [
    "TOPG",
    "ARENA_TOP_100",
    "GAME_TOOR",
    "OPSL",
    "PrivateServerWS"
]

token = "W8W1R67OM2UP84B06B81Y4G0"

def get_promote_timeout():    
    url = f"{config.server.host}/darkmatter/promote"
    headers_dict = { **headers }

    response = requests.get(url, headers=headers_dict, cookies=cookies)

    soup = BeautifulSoup(response.text, 'html.parser')
    time_text = soup.find('span', class_='x-vote-time').text
    h, m, s = map(int, time_text.split(':'))
    delta = timedelta(hours=h, minutes=m, seconds=s)

    return delta

def is_online_bonus_present():
    url = f"{config.server.host}/home"
    headers_dict = { **headers }

    response = requests.get(url, headers=headers_dict, cookies=cookies)

    soup = BeautifulSoup(response.text, 'html.parser')
    online_bonus = soup.find('span', class_='btn-online-bonus-anim')

    if online_bonus is None:
        return False
    
    return True

def visit_promote(provider, token):
    url = f"{config.server.host}/Darkmatter/PromoteOut"
    headers_dict = { **headers }

    params = { 
        "providerType": provider,
        "token": token
    }

    response = requests.get(url, headers=headers_dict, cookies=cookies, params=params)

def visit_all_promotes():
    for provider in providers:
        visit_promote(provider, token)

def online_bonus():
    url = f"{config.server.host}/home/onlinebonus"
    headers_dict = { **headers }

    response = requests.get(url, headers=headers_dict, cookies=cookies)
