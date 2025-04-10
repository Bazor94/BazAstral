from models import models
from services import colonize_planet
from EP import home
from EP import login
from EP import staticstics
import threading
from services import plunder
from EP import galaxy
from config import config
from services import build_defense
from services import fleet_service
from services import send_expedition
from EP import fleet
from logger import logger



models.planets = home.get_planets()

schuttgard = models.search_for_planet(models.planets, "6:219:11")
send_expedition.transport_resources_to_planet(schuttgard, 100000000000)




        