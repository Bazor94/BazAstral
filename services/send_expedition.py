from EP import fleet
import config
from datetime import datetime, timedelta
import logging
import helpers
import thread_lock

time_delay = 15

@thread_lock.locker(thread_lock.is_idle)
def send_expedition(planet):
    ships, referer_url = fleet.get_fleet(planet.moon_id)
    battle_ships = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] != 'ASTEROID_MINER' and ship['ShipType'] != 'LIGHT_CARGO']} 
    _, referer_url = fleet.get_autoexpedition_fleet(planet.moon_id, referer_url)
    fleet.send_autoexpedition_fleet(battle_ships, config.expedition_count, referer_url)


def send_expedition_cron(planet, stop_threads):
    while not stop_threads.is_set(): 
        expeditions = get_fleet_expedition_movement()
        while len(expeditions) > 0 and not stop_threads.is_set():
            exp = expeditions[-1]
            if exp.date_right is not None and exp.date_right > exp.date_left:
                time_sleep = int((exp.date_right - datetime.now()).total_seconds()) + time_delay
                logging.info(f'autoexpedition | sleeping for  {helpers.format_seconds(time_sleep)}. Till {datetime.now() +timedelta(seconds=time_sleep)} | date_right')
                stop_threads.wait(time_sleep)
            else:
                time_sleep = int((exp.date_left - datetime.now()).total_seconds()) + time_delay
                logging.info(f'autoexpedition | sleeping for  {helpers.format_seconds(time_sleep)}. Till {datetime.now() + timedelta(seconds=time_sleep)} | date_left')
                stop_threads.wait(time_sleep)

            expeditions = get_fleet_expedition_movement()
        
        if stop_threads.is_set():
            return

        logging.info(f'autoexpedition | sending autoexpedition')
        try:
            send_expedition(planet)
        except Exception as e:
            logging.warning(f'autoexpedition | autoexpedition error - {e}')
            stop_threads.wait(time_delay)
        

def get_fleet_expedition_movement():
    missions, _ = fleet.get_feet_movement()
    expeditions = [mission for mission in missions if mission.type in ['Expedition', 'Expedition (R)']]

    return expeditions
    
