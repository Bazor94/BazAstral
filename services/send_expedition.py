from EP import fleet
from config import config
from datetime import datetime, timedelta
import logging
import helpers
import threads
import time
from services import fleet as fleet_service
from logger import logger

time_delay = 15

@threads.locker(threads.is_idle)
def send_expedition(planet):
    ships, referer_url = fleet.get_fleet(planet.moon_id)
    battle_ships = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] != 'ASTEROID_MINER']} 
    _, referer_url = fleet.get_autoexpedition_fleet(planet.moon_id, referer_url)
    fleet.send_autoexpedition_fleet(battle_ships, config.crons.expedition.count, referer_url)
    threads.refresh_missions_gui.put("refresh")


def send_expedition_if_free(planet):
    expeditions = get_fleet_expedition_movement()

    if len(expeditions) > 0:
        exp = expeditions[-1]
        time_sleep = int((exp.back_date - datetime.now()).total_seconds()) + time_delay
        logger.info(f'initial sleeping for  {helpers.format_seconds(time_sleep)}. Till {datetime.now() +timedelta(seconds=time_sleep)}', extra={"planet": planet, "action": "expedition"})
        threads.stop_threads.wait(time_sleep)
        return

    logger.info(f'sending autoexpedition', extra={"planet": planet, "action": "expedition"})
    try:
        send_expedition(planet)
    except Exception as e:
        logging.warning(f'autoexpedition error - {e}', extra={"planet": planet, "action": "expedition"})
        threads.stop_threads.wait(time_delay)


def get_fleet_expedition_movement():
    expeditions = fleet_service.get_missions()['Expedition']

    return expeditions
