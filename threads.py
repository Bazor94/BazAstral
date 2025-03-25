import threading
import config

is_idle = threading.Event()
is_idle.set()

stop_threads = threading.Event()

running_threads = {}
for key, value in config.crons.items():
    running_threads[key] = threading.Event()
    running_threads[key].set() if value else running_threads[key].clear()


def locker(is_idle):
    def decorator(func):
        def wrapper(*args, **kwargs):
            is_idle.wait(60)
            is_idle.clear()

            try:
                return func(*args, **kwargs) 
            finally:
                is_idle.set()
            
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