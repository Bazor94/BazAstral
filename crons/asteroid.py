import threading
from config import config
import threads
from services.mine_asteroid import send_miners


@threads.stoper(threads.stop_threads, threads.running_threads['asteroid'])
def mine_asteroids_single_planet(planet, is_asteroid_taken, is_from_moon):
    send_miners(planet, is_asteroid_taken, is_from_moon)


def mine_asteroids_cron(planets, is_from_moon):
    is_asteroid_taken = {}
    threads = []

    for planet in planets:
        thread = threading.Thread(target=mine_asteroids_single_planet, args=(planet, is_asteroid_taken, is_from_moon))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


class SharedValue:
    def __init__(self, value):
        self.value = value
        self.lock = threading.Lock()

    def decrement(self, value):
        with self.lock:
            self.value -= value