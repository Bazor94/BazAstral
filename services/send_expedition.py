from EP import fleet
import config
from datetime import datetime, timedelta
import logging
import helpers
import threads
import time
from services import fleet as fleet_service

time_delay = 15

@threads.locker(threads.is_idle)
def send_expedition(planet):
    ships, referer_url = fleet.get_fleet(planet.moon_id)
    battle_ships = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] != 'ASTEROID_MINER']} 
    _, referer_url = fleet.get_autoexpedition_fleet(planet.moon_id, referer_url)
    fleet.send_autoexpedition_fleet(battle_ships, config.expedition_count, referer_url)


def send_expedition_if_free(planet):
    expeditions = get_fleet_expedition_movement()

    if len(expeditions) > 0:
        exp = expeditions[-1]
        time_sleep = int((exp.back_date - datetime.now()).total_seconds()) + time_delay
        logging.info(f'autoexpedition | {planet.coords} | sleeping for  {helpers.format_seconds(time_sleep)}. Till {datetime.now() +timedelta(seconds=time_sleep)}')
        threads.stop_threads.wait(time_sleep)
        return

    logging.info(f'autoexpedition | sending autoexpedition')
    try:
        send_expedition(planet)
    except Exception as e:
        logging.warning(f'autoexpedition | autoexpedition error - {e}')
        threads.stop_threads.wait(time_delay)


def get_fleet_expedition_movement():
    expeditions = fleet_service.get_missions()['Expedition']

    return expeditions
