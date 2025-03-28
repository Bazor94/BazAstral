from config import config
import EP.login as login
from EP import home
import threading
import time
import models.planet as p
from models import planet
import threads
from crons import asteroid
from crons import expedition
from crons import refresh
from crons import collect
from crons import defense
from crons import bonus
from services import build_defense

def run_crons():
    threads_list = []

    # login cron
    threads_list.append(threading.Thread(target=refresh.refresh_cron, args=()))
    threads_list[-1].start()

    # planets
    planet.planets = home.get_planets()
    planets = []
    for coord in config.crons.asteroid.coords:
        planets.append(p.search_for_planet(planet.planets, coord))

    # build_defense.build_max_platforms_all_planets(planet.planets)

    # asteroids cron
    threads_list.append(threading.Thread(target=asteroid.mine_asteroids_cron, args=(planets, config.crons.asteroid.fs, config.crons.asteroid.is_from_moon)))

    # expedition
    main_planet = p.search_for_planet(planet.planets, config.crons.asteroid.coords[0])
    threads_list.append(threading.Thread(target=expedition.send_expedition_cron, args=(main_planet,)))

    # collect resources cron
    main_planet = p.search_for_planet(planet.planets, config.crons.asteroid.coords[0])
    other_planets = [p for p in planet.planets if p.id != main_planet.id]
    threads_list.append(threading.Thread(target=collect.collect_all_resources_cron, args=(main_planet, other_planets)))

    # building defense cron
    threads_list.append(threading.Thread(target=defense.build_def_cron, args=(main_planet,)))

    # bonus cron
    threads_list.append(threading.Thread(target=bonus.promote_cron, args=()))
    threads_list.append(threading.Thread(target=bonus.online_bonus_cron, args=()))


    for i, thread in enumerate(threads_list):
        if i > 0: # nie startuj pierwszego threada czyli refresh
            thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Przerywam program...")
        threads.stop_threads.set() 
        for thread in threads_list:
            thread.join()
        print("Wątki zakończone.")

