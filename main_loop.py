import config
import EP.login as login
from EP import home
import threading
import time
import models.planet as p
from models import planet
from services import send_expedition
from services import mine_asteroid
import threads

def run_crons():
    threads_list = []

    # login cron
    #driver = login.login()
    #threads.running_threads['login'] = threading.Event()
    #threads_list.append(threading.Thread(target=login.refresh_cron, args=(driver,)))

    # planets
    planet.planets = home.get_planets()
    planets = []
    for coord in config.coords:
        planets.append(p.search_for_planet(planet.planets, coord))

        
    # build_defense.build_max_platforms_all_planets(all_planets)

    # asteroids cron
    threads_list.append(threading.Thread(target=mine_asteroid.mine_asteroids_cron, args=(planets, config.fs)))

    # expedition
    main_planet = p.search_for_planet(planet.planets, config.coords[0])
    threads_list.append(threading.Thread(target=send_expedition.send_expedition_cron, args=(main_planet,)))

    # collect resources cron
    # main_planet = p.search_for_planet(all_planets, config.coords[0])
    # other_planets = [p for p in all_planets if p.id != main_planet.id]
    # threads_list.append(threading.Thread(target=collect_resources.collect_all_resources_cron, args=(main_planet, other_planets, 3 * 3600)))

    # building defense cron
    # threads_list.append(threading.Thread(target=build_defense.build_def_cron, args=(main_planet, 3 * 3600)))

    threads_list.append(threading.Thread(target=send_expedition.sron, args=()))

    # threads.running_threads['asteroid'].set()
    

    for thread in threads_list:
        thread.start()


    threads.running_threads['sron'].set()
    threading.Timer(5, threads.running_threads['sron'].clear).start()
    threading.Timer(10, threads.running_threads['sron'].set).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Przerywam program...")
        threads.stop_threads.set() 
        for thread in threads_list:
            thread.join()
        print("Wątki zakończone.")

