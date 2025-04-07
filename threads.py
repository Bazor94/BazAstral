import threading
from config import config
import queue

mutex = threading.Lock()

stop_threads = threading.Event()

refresh_missions_gui = queue.Queue()

running_threads = {}
for key, value in config.crons.dict().items():
    running_threads[key] = threading.Event()
    running_threads[key].set() if value['enabled'] else running_threads[key].clear()


def locker():
    def decorator(func):
        def wrapper(*args, **kwargs):
            with mutex:
                return func(*args, **kwargs) 
            
        return wrapper
    return decorator

def stoper(stop_threads, running_thread):
    def decorator(func):
        def wrapper(*args, **kwargs):
            while not stop_threads.is_set(): 
                if not running_thread.is_set():
                    stop_threads.wait(1)
                    continue
                
                func(*args, **kwargs) 
        return wrapper
    return decorator