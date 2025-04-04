from EP import fleet
from config import config
from datetime import datetime, timedelta
import logging
import helpers
import threads
import time
from services import fleet_service
from logger import logger
import math
from models import models

time_delay = 15

@threads.locker(threads.is_idle)
def old_send_expedition(planet):
    ships, referer_url = fleet.get_fleet(planet.moon_id)
    battle_ships = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] != 'ASTEROID_MINER']} 
    _, referer_url = fleet.get_autoexpedition_fleet(planet.moon_id, referer_url)
    fleet.send_autoexpedition_fleet(battle_ships, config.crons.expedition.count, referer_url)
    threads.refresh_missions_gui.put("refresh")


def old_send_expedition_if_free(planet):
    expeditions = get_fleet_expedition_movement()

    if len(expeditions) > 0:
        exp = expeditions[-1]
        time_sleep = int((exp.back_date - datetime.now()).total_seconds()) + time_delay
        logger.info(f'initial sleeping for  {helpers.format_seconds(time_sleep)}. Till {datetime.now() +timedelta(seconds=time_sleep)}', extra={"planet": planet, "action": "expedition"})
        threads.stop_threads.wait(time_sleep)
        return

    logger.info(f'sending autoexpedition', extra={"planet": planet, "action": "expedition"})
    try:
        old_send_expedition(planet)
    except Exception as e:
        logging.warning(f'autoexpedition error - {e}', extra={"planet": planet, "action": "expedition"})
        threads.stop_threads.wait(time_delay)


def send_expedition_if_free(planet):
    expeditions = get_planet_fleet_expedition_movement(planet)

    if len(expeditions) > 0:
        exp = expeditions[-1]
        time_sleep = int((exp.back_date - datetime.now()).total_seconds()) + time_delay
        logger.info(f'initial sleeping for  {helpers.format_seconds(time_sleep)}. Till {datetime.now() +timedelta(seconds=time_sleep)}', extra={"planet": planet, "action": "expedition"})
        threads.stop_threads.wait(time_sleep)
        return

    logger.info(f'sending expedition', extra={"planet": planet, "action": "expedition"})
    try:
        fleet_service.send_expedition_with_resources(planet, config.crons.expedition.time)
    except Exception as e:
        logging.warning(f'expedition error - {e}', extra={"planet": planet, "action": "expedition"})
        threads.stop_threads.wait(time_delay)


def get_fleet_expedition_movement():
    expeditions = fleet_service.get_missions()['Expedition']

    return expeditions


def get_planet_fleet_expedition_movement(planet):
    expeditions = fleet_service.get_missions()['Expedition']
    planet_exps = [e for e in expeditions if e.planet == planet]

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
        