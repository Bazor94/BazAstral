import config
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
from services import build_defense
from logger import logger  # Dodany import loggera

def run_crons():
    threads_list = []

    # login cron
    threads_list.append(threading.Thread(target=refresh.refresh_cron, args=()))
    threads_list[-1].start()

    # planets
    planet.planets = home.get_planets()
    planets = []
    for coord in config.coords:
        planets.append(p.search_for_planet(planet.planets, coord))

    # asteroids cron
    threads_list.append(threading.Thread(target=asteroid.mine_asteroids_cron, args=(planets, config.fs, config.asteroid_is_from_moon)))

    # expedition
    main_planet = p.search_for_planet(planet.planets, config.coords[0])
    threads_list.append(threading.Thread(target=expedition.send_expedition_cron, args=(main_planet,)))

    # collect resources cron
    main_planet = p.search_for_planet(planet.planets, config.coords[0])
    other_planets = [p for p in planet.planets if p.id != main_planet.id]
    threads_list.append(threading.Thread(target=collect.collect_all_resources_cron, args=(main_planet, other_planets, 3 * 3600)))

    # building defense cron
    threads_list.append(threading.Thread(target=defense.build_def_cron, args=(main_planet, 3 * 3600)))

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
        
        # Dodane zamknięcie handlerów loggera
        for handler in logger.handlers[:]:  # Iterujemy po kopii listy
            try:
                if hasattr(handler, 'close'):
                    handler.close()
                logger.removeHandler(handler)  # Usuwamy handler z loggera
            except Exception as e:
                print(f"Błąd przy zamykaniu handlera: {e}")
        
        print("Wątki zakończone.")