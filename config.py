import yaml

from pydantic import BaseModel
import yaml

class Collect(BaseModel):
    enabled: bool
    interval: int

class Bonus(BaseModel):
    enabled: bool

class Refresh(BaseModel):
    enabled: bool 
    interval: int

class Asteroid(BaseModel):
    enabled: bool
    is_from_moon: bool
    coords: list
    fs: list
    miners_percentage: int
    miners_speed: int

class Defense(BaseModel):
    enabled: bool
    interval: int

class Expedition(BaseModel):
    enabled: bool
    count: int

class Crons(BaseModel):
    asteroid: Asteroid
    collect: Collect
    defense: Defense
    expedition: Expedition
    refresh: Refresh
    bonus: Bonus

class Server(BaseModel):
    fleet_speed: int
    host: str

class Creds(BaseModel):
    login: str
    password: str
    cf_clearance: str
    game_auth_token: str
    session_id: str

class Config(BaseModel):
    creds: Creds
    server: Server
    crons: Crons

# === FUNKCJE ZAPISU/ODCZYTU ===
def load_config(path="config.yaml") -> Config:
    with open(path, "r") as file:
        data = yaml.safe_load(file)
    return Config(**data)

def save_config(path="config.yaml"):
    with open(path, "w") as file:
        yaml.safe_dump(config.dict(), file, default_flow_style=False)


config = load_config()

cookies = {
    'SessionId': config.creds.session_id,
    'gameAuthToken': config.creds.game_auth_token,
    'cf_clearance': config.creds.cf_clearance,
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
