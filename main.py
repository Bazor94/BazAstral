import config
import EP.login as login
import mine_asteroid
from EP import home
from EP import fleet
import threading
import time
import planet as p

stop_threads = threading.Event()

driver = login.login()
t1 = threading.Thread(target=login.refresh_cron, args=(driver, stop_threads))
t1.start()

all_planets = home.get_planets()
planets = []
for coord in config.coords:
    planets.append(p.search_for_planet(all_planets, coord))

t2 = threading.Thread(target=mine_asteroid.mine_asteroids_cron, args=(planets, config.fs, stop_threads))
t2.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Przerywam program...")
    stop_threads.set() 
    t1.join()  # Czekamy na zakończenie wątku
    t2.join()
    print("Wątki zakończone.")
