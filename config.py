import yaml
import logging

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

login = config.get("login")
password = config.get("password")
session_id = config.get("session_id")
game_auth_token = config.get("game_auth_token")
cf_clearance = config.get("cf_clearance")
host = config.get("host")
coords = config.get("coords")
fleet_speed = config.get("fleet_speed")

logging.basicConfig(
    level=logging.INFO,  # Ustalamy minimalny poziom logowania (DEBUG oznacza, że będą rejestrowane wszystkie logi)
    format='%(asctime)s - %(levelname)s: %(message)s',  # Ustalamy format logu
)

cookies = {
    'SessionId': session_id,
    'gameAuthToken': game_auth_token,
    'cf_clearance': cf_clearance,
    'lang': 'en',
    'timeZoneOffset': '60',
    '_gid': 'GA1.2.441450251.1739041032',
    '_ga': 'GA1.1.38274606.1739041032',
    '_ga_65PNDYM0LK': 'GS1.1.1739048141.3.0.1739048141.60.0.0'
}

headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en",
        "priority": "u=0, i",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132")',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }
