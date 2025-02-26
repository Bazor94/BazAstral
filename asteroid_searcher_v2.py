import EP.galaxydata as galaxydata
import EP.galaxy as galaxy
from EP import partial_asteroid
import time
import random
import helpers
import logging

def get_closest_asteroid_range(ranges, y):
    min_dist = 999
    closest_asteroid = 0
    for i, range in enumerate(ranges):
        avg = (range[0] + range[1]) / 2
        if abs(y - avg) < min_dist:
            min_dist = abs(y - avg)
            closest_asteroid = i

    return ranges[closest_asteroid]

def get_asteroid_y(x, y_from, y_to):
    _, referal_url = galaxy.get_galaxy_html() # only for referal_url purposes (anti_bot?)

    for i in range(y_from, y_to):
        time.sleep(random.uniform(0.25, 0.5))

        is_asteroid, url, time_left, referal_url = galaxydata.get_asteroid(referal_url, x, i)
        if is_asteroid:
            time_parsed = time_left.strip("()").split(":")
            seconds_left = int(time_parsed[0]) * 60 + int(time_parsed[1])
            return i, seconds_left

    return None, None


def get_closest_asteroid(x, y, z):
    _, referal_url = galaxy.get_galaxy_html()
    ranges = partial_asteroid.get_asteroid_locations(referal_url)
    logging.info(f'found ranges: {ranges}')

    while len(ranges) > 0:
        closest_asteroid_range = get_closest_asteroid_range(ranges, y)
        logging.info(f'found closest range:{closest_asteroid_range}')
        asteroid_y, time_left = get_asteroid_y(x, closest_asteroid_range[0], closest_asteroid_range[1])
        time_needed = helpers.calculate_time(x, y, z, x, asteroid_y, 16, 30160, 10) #TODO put speed to config
        if time_needed < time_left - 15:
            logging.info(f'not enough time for asteroid {asteroid_y} | time left: {time_left}, needed: {time_needed}')
            ranges.remove(closest_asteroid_range)
        else:
            logging.info(f'going for asteroid: {x}:{asteroid_y}:17')
            return asteroid_y, time_needed
    
    logging.info('cannot find asteroid')
    return None, None
    



