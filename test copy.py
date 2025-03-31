from services import colonize_planet
from EP import home
from models import planet
from EP import login
from EP import staticstics
import threading
from services import farm_idles
from EP import galaxydata
from config import config

stats = farm_idles.get_player_ranks()
galaxydata.get_plunder_ids(6, 367, stats, 1000, config.server.host+"/home")
galaxydata.send_plunder()
