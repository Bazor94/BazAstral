import requests
from config import config, headers, cookies
from bs4 import BeautifulSoup
from logger import logger
from datetime import timedelta
import urllib.parse as urlparse

providers = [
    "TOPG",
    "ARENA_TOP_100",
    "GAME_TOOR",
    "OPSL",
    "PrivateServerWS"
]

def get_promote_timeout():    
    url = f"{config.server.host}/darkmatter/promote"
    headers_dict = { **headers }

    response = requests.get(url, headers=headers_dict, cookies=cookies)

    soup = BeautifulSoup(response.text, 'html.parser')

    provider_vote = soup.find('div', class_='provider-vote')
    provider_vote = provider_vote.find('a')
    if provider_vote is not None:
        link = provider_vote['href']
        parsed_url = urlparse.urlparse(link)
        token = urlparse.parse_qs(parsed_url.query).get('token', [None])[0]
        return token, None

    
    time_text_span = soup.find('span', class_='x-vote-time')
    if time_text_span == None:
        return None, None
    
    t = time_text_span.text.split(':')
    if len(t) == 3:
        delta = timedelta(hours=int(t[0]), minutes=int(t[1]), seconds=int(t[2]))
    elif len(t) == 2:
        delta = timedelta(minutes=int(t[0]), seconds=int(t[1]))
    elif len(t) == 1:
        delta = timedelta(seconds=int(t[0]))

    return None, delta

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

def visit_all_promotes(token):
    for provider in providers:
        visit_promote(provider, token)

def online_bonus():
    url = f"{config.server.host}/home/onlinebonus"
    headers_dict = { **headers }

    response = requests.get(url, headers=headers_dict, cookies=cookies)
