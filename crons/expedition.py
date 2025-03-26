import threading
import config
import threads
from services.send_expedition import send_expedition_if_free


@threads.stoper(threads.stop_threads, threads.running_threads['expedition'])
def send_expedition_cron(planet):
    send_expedition_if_free(planet)
