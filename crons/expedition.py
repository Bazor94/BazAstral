import threading
from config import config
import threads
from services import send_expedition
import time


@threads.stoper(threads.stop_threads, threads.running_threads['expedition'])
def send_expedition_single_cron(planet):
    send_expedition.send_expedition_if_free(planet)

def send_expedition_cron(planets):
    threads = []

    for planet in planets:
        thread = threading.Thread(target=send_expedition_single_cron, args=(planet,))
        threads.append(thread)
        time.sleep(15)
        thread.start()

    for thread in threads:
        thread.join()
