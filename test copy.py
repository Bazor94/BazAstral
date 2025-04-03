from services import colonize_planet
from EP import home
from models import planet
from EP import login
from EP import staticstics
import threading
from services import plunder
from EP import galaxydata
from config import config
from services import build_defense
from services import fleet as fleet_service
from services import send_expedition
from EP import fleet
from logger import logger


def get_planets_from_coords(planet_coords):
    planets = []

    for planet_coord in planet_coords:
        planet_object = planet.search_for_planet(planet.planets, planet_coord)
        if planet_object is None:
            logger.error(f"cannot find planet {planet_coords}. Planets len: {len(planets)}")
            continue

        planets.append(planet_object)

    return planets

planet.planets = home.get_planets()
# ranks = plunder.get_player_ranks()
# plunder.plunder_galaxy(planet.planets[1], ranks, 800, 6, 1, 499, 45)
#build_defense.build_max_platforms_all_planets(planet.planets[0:11])


planets = get_planets_from_coords(config.crons.expedition.planets)
send_expedition.deploy_split_ships(planets, planet.planets[1])



        