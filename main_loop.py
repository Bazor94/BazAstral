from config import config
import EP.login as login
from EP import home
import threading
import time
from models import models
import threads
from crons import asteroid, expedition, plunder, refresh, collect, defense, bonus
from services import build_defense

def run_crons():
    threads_list = []

    # login cron
    threads_list.append(threading.Thread(target=refresh.refresh_cron, args=()))
    threads_list[-1].start()

    # planets
    models.planets = home.get_planets()
    planets = []
    for coord in config.crons.asteroid.coords:
        planets.append(models.search_for_planet(models.planets, coord))

    build_defense.build_max_platforms_all_planets(models.planets)

    # asteroids cron
    threads_list.append(threading.Thread(target=asteroid.mine_asteroids_cron, args=(planets, config.crons.asteroid.fs, config.crons.asteroid.is_from_moon)))

    # expedition
    main_planet = models.search_for_planet(models.planets, config.crons.expedition.planets[0])
    threads_list.append(threading.Thread(target=expedition.send_expedition_cron, args=(main_planet,)))

    # plunder cron
    threads_list.append(threading.Thread(target=plunder.plunder_cron))

    # collect resources cron
    main_planet = models.search_for_planet(models.planets, config.crons.asteroid.coords[0])
    other_planets = [p for p in models.planets if p.id != main_planet.id]
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

