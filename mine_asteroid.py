import asteroid_searcher_v2
import send_fleet
import datetime
import logging
import helpers
import threading
import config

time_delay_seconds = 15

def mine_asteroids_single_planet(planet, fs, stop_threads, is_asteroid_taken):
    x, y, z, moon_id = planet.x, planet.y, planet.z, planet.moon_id

    while not stop_threads.is_set(): 
        asteroid_y, time_needed = asteroid_searcher_v2.get_closest_asteroid(x, y, z, is_asteroid_taken)
        if asteroid_y != None:
            logging.info(f'{x}:{y}:{z} | sending miners for asteroid {x}:{asteroid_y}:17, time needed: {helpers.format_seconds(time_needed)}')
            send_fleet.send_full_miners(x, asteroid_y, moon_id)
            time_sleep = time_needed * 2 + time_delay_seconds
        else:
            # fs_x, fs_y, fs_z = map(int, fs.split(':')) TODO bring this back
            # fs_time = 2 * helpers.calculate_time(x, y, z, fs_x, fs_y, fs_z, config.miners_speed, 100)
            # logging.info(f'{x}:{y}:{z} | sending fs to {fs}. Fleet time: {helpers.format_seconds(fs_time)}')
            # send_fleet.send_full_miners_fs(fs_x, fs_y, fs_z, moon_id)

            # time_sleep = fs_time + time_delay_seconds
            time_sleep = 120

        logging.info(f'{x}:{y}:{z} | sleeping for {helpers.format_seconds(time_sleep)}. Till {datetime.datetime.now() + datetime.timedelta(seconds=time_sleep)}')
        stop_threads.wait(time_sleep)
        is_asteroid_taken[asteroid_y] = False


def mine_asteroids_cron(planets, fses, stop_threads):
    is_asteroid_taken = {}
    threads = []
    for planet, fs in zip(planets, fses):
        print(planet)
        thread = threading.Thread(target=mine_asteroids_single_planet, args=(planet, fs, stop_threads, is_asteroid_taken))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

