from EP import fleet
from config import config
from datetime import datetime
import threads
from services import fleet_service
from logger import logger
import math
from models import models

time_delay = 15
time_exception_delay=120


def get_planets_from_coords(planet_coords):
    planets = []

    for planet_coord in planet_coords:
        planet_object = models.search_for_planet(models.planets, planet_coord)
        if planet_object is None:
            logger.error(f"cannot find planet {planet_coords}. Planets len: {len(planets)}")
            continue

        planets.append(planet_object)

    return planets


def send_expedition_if_free(planet):
    expeditions = get_planet_fleet_expedition_movement(planet)

    if len(expeditions) > 0:
        exp = expeditions[-1]
        time_sleep = int((exp.back_date - datetime.now()).total_seconds()) + time_delay
        logger.sleep_log("expedition", planet, time_sleep)
        threads.stop_threads.wait(time_sleep)
        return
    
    _, resources, _ = fleet.get_fleet_and_resources(planet.moon_id)
    if resources.deuterium < config.crons.expedition.wanted_deuterium / 2:
        logger.warning(f'Low deuterium on {planet} - {resources.deuterium:,}')
        resources.deuterium = 0
    
    if config.crons.expedition.send_resources:
        try:
            transport_resources_to_planet(planet, config.crons.expedition.wanted_deuterium)
            threads.stop_threads.wait(40)
        except Exception as e:
            pass

    logger.info(f'sending expedition', extra={"planet": planet, "action": "expedition"})
    
    try:
        fleet_service.send_expedition_with_resources(planet, config.crons.expedition.time)
        threads.refresh_missions_gui.put("refresh")
    except Exception as e:
        logger.warning(f'expedition error - {e}', extra={"planet": planet, "action": "expedition"})
        threads.stop_threads.wait(time_exception_delay)


def transport_resources_to_planet(planet, wanted_deuterium):
    _, resources, _ = fleet.get_fleet_and_resources(planet.moon_id)
    
    if resources.deuterium < wanted_deuterium:
        resources.deuterium = 0
    else:
        resources.deuterium = resources.deuterium - wanted_deuterium

    logger.info(f'sent resources: {resources}', extra={"planet": planet, "action": "expedition"})

    x, y, z = planet.x, planet.y, planet.z
    fleet_service.transport_resources(planet, True, x, y, z, False, resources)


def get_fleet_expedition_movement():
    expeditions = fleet_service.get_missions()['Expedition']

    return expeditions


def get_planet_fleet_expedition_movement(planet):
    expeditions = fleet_service.get_missions()['Expedition']
    planet_exps = [e for e in expeditions if e.planet.coords == planet.coords]

    return planet_exps


def deploy_split_ships(planets, main_planet):
    ships, _ = fleet.get_fleet(main_planet.moon_id)
    ships = ships['Ships']
    planet_ships = calc_split_ships(ships, planets)
    planets.remove(main_planet)

    for planet in planets:
        ships_to_deploy = planet_ships[planet.coords]
        fleet_service.deploy_ships(main_planet, planet, ships_to_deploy)


def calc_split_ships(ships, planets):
    planets_num = len(planets)
    planet_ships = {}
    for i, planet in enumerate(planets):
        planet_ships[planet.coords] = []

        for ship in ships:
            quantity = math.floor(ship['Quantity'] / planets_num)
            if ship['Quantity'] % planets_num >= i + 1:
                quantity += 1
            
            planet_ships[planet.coords].append({"ShipType": ship["ShipType"], "Quantity": quantity})

    return planet_ships

        

# @threads.locker(threads.is_idle)
# def old_send_expedition(planet):
#     ships, referer_url = fleet.get_fleet(planet.moon_id)
#     battle_ships = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] != 'ASTEROID_MINER']} 
#     _, referer_url = fleet.get_autoexpedition_fleet(planet.moon_id, referer_url)
#     fleet.send_autoexpedition_fleet(battle_ships, config.crons.expedition.count, referer_url)
#     threads.refresh_missions_gui.put("refresh")


# def old_send_expedition_if_free(planet):
#     expeditions = get_fleet_expedition_movement()

#     if len(expeditions) > 0:
#         exp = expeditions[-1]
#         time_sleep = int((exp.back_date - datetime.now()).total_seconds()) + time_delay
#         logger.info(f'initial sleeping for  {helpers.format_seconds(time_sleep)}. Till {datetime.now() +timedelta(seconds=time_sleep)}', extra={"planet": planet, "action": "expedition"})
#         threads.stop_threads.wait(time_sleep)
#         return

#     logger.info(f'sending autoexpedition', extra={"planet": planet, "action": "expedition"})
#     try:
#         old_send_expedition(planet)
#     except Exception as e:
#         logging.warning(f'autoexpedition error - {e}', extra={"planet": planet, "action": "expedition"})
#         threads.stop_threads.wait(time_delay)
