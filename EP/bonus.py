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

    provider_vote_divs = soup.find_all('div', class_='provider-vote')

    max_delta_time = timedelta()
    tokens = []
    for provider_vote_div in provider_vote_divs:
        provider_vote = provider_vote_div.find('a')
        if provider_vote is not None:
            link = provider_vote['href']
            parsed_url = urlparse.urlparse(link)
            token = urlparse.parse_qs(parsed_url.query).get('token', [None])[0]
            tokens.append(token)

            continue

        time_text_span = soup.find('span', class_='x-vote-time')
        if time_text_span == None:
            continue

        t = time_text_span.text.split(':')
        if len(t) == 3:
            delta = timedelta(hours=int(t[0]), minutes=int(t[1]), seconds=int(t[2]))
        elif len(t) == 2:
            delta = timedelta(minutes=int(t[0]), seconds=int(t[1]))
        elif len(t) == 1:
            delta = timedelta(seconds=int(t[0]))

        if delta > max_delta_time:
            max_delta_time = delta

    if len(tokens) == 5:
        return tokens, None

    return None, max_delta_time

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

def visit_all_promotes(tokens):
    for provider, token in zip(providers, tokens):
        visit_promote(provider, token)

def online_bonus():
    url = f"{config.server.host}/home/onlinebonus"
    headers_dict = { **headers }

    response = requests.get(url, headers=headers_dict, cookies=cookies)
