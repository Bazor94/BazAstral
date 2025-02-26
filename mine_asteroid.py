import asteroid_searcher_v2
import send_fleet
import time
import datetime
import logging
import helpers

def mine_asteroid(x, y, z):
    asteroid_y, time_needed = asteroid_searcher_v2.get_closest_asteroid(x, y, z)
    if asteroid_y != None:
        logging.info(f'sending miners for asteroid {x}:{asteroid_y}:17, time needed: {helpers.format_seconds(time_needed)}')
        send_fleet.send_full_miners(x, asteroid_y, 17)
        return time_needed * 2
    else:
        return None


def mine_asteroids_cron(x, y, z):
    while True: 
        fleet_not_available_time = mine_asteroid(x, y, z)
        if fleet_not_available_time != None:
            time_sleep = fleet_not_available_time + 15 
            logging.info(f'sleeping for {helpers.format_seconds(time_sleep)}. Till {datetime.datetime.now() + datetime.timedelta(seconds=time_sleep)}')
            time.sleep(time_sleep)
        else:
            time_sleep = 5 * 60
            logging.info(f'sleeping for {helpers.format_seconds(time_sleep)}. Till {datetime.datetime.now() + datetime.timedelta(seconds=time_sleep)}')
            time.sleep(time_sleep)


    
