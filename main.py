import config
import EP.login as login
import services.mine_asteroid as mine_asteroid
from EP import home
from EP import fleet
import threading
import time
import models.planet as p
import services.build_defense as build_defense
import services.collect_resources as collect_resources
import services.send_expedition as send_expedition

stop_threads = threading.Event()
is_idle = threading.Event()

# login cron
driver = login.login()
t1 = threading.Thread(target=login.refresh_cron, args=(driver, stop_threads))
t1.start()

# planets
all_planets = home.get_planets()
planets = []
for coord in config.coords:
    planets.append(p.search_for_planet(all_planets, coord))

    
# build_defense.build_max_platforms_all_planets(all_planets)

# asteroids cron
t2 = threading.Thread(target=mine_asteroid.mine_asteroids_cron, args=(planets, config.fs, stop_threads))
t2.start()

# expedition
main_planet = p.search_for_planet(all_planets, config.coords[0])
t3 = threading.Thread(target=send_expedition.send_expedition_cron, args=(main_planet, stop_threads))
t3.start()

# collect resources cron
# main_planet = p.search_for_planet(all_planets, config.coords[0])
# other_planets = [p for p in all_planets if p.id != main_planet.id]
# t4 = threading.Thread(target=collect_resources.collect_all_resources_cron, args=(main_planet, other_planets, 3 * 3600, stop_threads))
# t4.start()

# building defense cron
# t5 = threading.Thread(target=build_defense.build_def_cron, args=(main_planet, 3 * 3600, stop_threads))
# t5.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Przerywam program...")
    stop_threads.set() 
    t1.join()
    t2.join()
    t3.join()
    # t4.join()
    # t5.join()
    print("Wątki zakończone.")

