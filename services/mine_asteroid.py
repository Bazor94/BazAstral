from datetime import datetime, timedelta, time
import logging
import helpers
import threading
from config import config, save_config
import EP.galaxy as galaxy
from EP import fleet
from services import fleet_service as fleet_service
import threads
from logger import logger

time_delay_seconds = 15
idle_time = 5 * 60

def get_closest_asteroid_range(ranges, y):
    min_dist = 999
    closest_asteroid = 0
    for i, range in enumerate(ranges):
        avg = (range[0] + range[1]) / 2
        if abs(y - avg) < min_dist:
            min_dist = abs(y - avg)
            closest_asteroid = i

    return ranges[closest_asteroid]

def get_asteroid_y(x, y_from, y_to, planet_id):
    _, referal_url = galaxy.get_galaxy_html() # only for referal_url purposes (anti_bot?)

    for i in range(y_from, y_to + 1):
        time_left, referal_url = galaxy.get_asteroid(referal_url, x, i, planet_id)
        if time_left is not None:
            time_parsed = time_left.strip("()").split(":")
            if len(time_parsed) == 1:
                seconds_left = int(time_parsed[0])
            elif len(time_parsed) == 2:
                seconds_left = int(time_parsed[0]) * 60 + int(time_parsed[1])
            elif len(time_parsed) == 3:
                seconds_left = int(time_parsed[0]) * 3600 + int(time_parsed[0]) * 60 + int(time_parsed[1])
            return i, seconds_left

    return None, None

@threads.locker()
def get_closest_asteroid(p, is_asteroid_taken):
    _, referal_url = galaxy.get_galaxy_html()
    ranges = galaxy.get_asteroid_locations(referal_url)

    while len(ranges) > 0:
        closest_asteroid_range = get_closest_asteroid_range(ranges, p.y)
        asteroid_y, time_left = get_asteroid_y(p.x, closest_asteroid_range[0], closest_asteroid_range[1], p.id)
        logger.info(f'ranges {ranges} - closest range:{closest_asteroid_range} - y: {asteroid_y}', extra={"planet": p, "action": "asteroid"})
        
        if asteroid_y is None:
            continue
        
        time_needed = helpers.calculate_time(p.x, p.y, p.z, p.x, asteroid_y, 17, config.crons.asteroid.miners_speed, 100)
        if time_needed > time_left - 15:
            logging.info(f'not enough time for asteroid {asteroid_y} | time left: {time_left}, needed: {time_needed}', extra={"planet": p, "action": "asteroid"})
            ranges.remove(closest_asteroid_range)
        elif is_asteroid_taken.get(asteroid_y):
            logging.info(f'asteroid {asteroid_y} is already taken - taken asteroids: {is_asteroid_taken}', extra={"planet": p, "action": "asteroid"})
            ranges.remove(closest_asteroid_range)
        else:
            logging.debug(f'correct - returning asteroid y', extra={"planet": p, "action": "asteroid"})
            return asteroid_y, time_needed
    
    logging.info('cannot find asteroid', extra={"planet": p, "action": "asteroid"})
    return None, None

        
def get_fleet_asteroids_movement(planet):
    missions = fleet_service.get_missions()['Asteroid Mining']
    asteroid_missions = [mission for mission in missions if mission.planet.coords == planet.coords]

    return asteroid_missions


def send_miners(planet, is_asteroid_taken, is_from_moon):
    base_id = planet.moon_id if is_from_moon else planet.id
    missions = get_fleet_asteroids_movement(planet)


    if time(0, 30) <= datetime.now().time() <= time(1, 0):
        config.crons.asteroid.miners_percentage = 100
        save_config()
    
    if len(missions) != 0:
        mission = missions[-1]
        time_sleep = int((mission.back_date - datetime.now()).total_seconds()) + time_delay_seconds
        logger.sleep_log("asteroid", planet, time_sleep, prefix="initial")
        threads.stop_threads.wait(time_sleep)
        
    asteroid_y, time_needed = get_closest_asteroid(planet, is_asteroid_taken)
    if asteroid_y != None:
        is_asteroid_taken[asteroid_y] = True
        logger.info(f'sending miners for asteroid {planet.x}:{asteroid_y}:17, time needed: {helpers.format_seconds(time_needed)}', extra={"planet": planet, "action": "asteroid"})
        
        try:
            fleet_service.send_full_miners(planet.x, asteroid_y, base_id, config.crons.asteroid.miners_percentage)
            logger.debug(f'sent miners for asteroid {planet.x}:{asteroid_y}:17, time needed: {helpers.format_seconds(time_needed)}', extra={"planet": planet, "action": "asteroid"})
        except Exception as e:
            is_asteroid_taken[asteroid_y] = False
            logger.warning(f'Mining Exception: {e}. Continue', extra={"planet": planet, "action": "asteroid"})

            time_sleep = idle_time
            logger.sleep_log("asteroid", planet, time_sleep, prefix="exception")
            threads.stop_threads.wait(time_sleep)
            return
        
        if config.crons.asteroid.miners_percentage > 40:
            config.crons.asteroid.miners_percentage -= 2
            save_config()
        time_sleep = time_needed * 2 + time_delay_seconds
    
    else:
        logger.warning(f'miners waiting', extra={"planet": planet, "action": "asteroid"})
        time_sleep = idle_time


    logger.sleep_log("asteroid", planet, time_sleep)
    threads.stop_threads.wait(time_sleep)
    is_asteroid_taken[asteroid_y] = False
