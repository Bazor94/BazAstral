import threading

is_idle = threading.Event()
is_idle.set()

stop_threads = threading.Event()
running_threads = {}
running_threads['asteroid'] = threading.Event()
running_threads['expedition'] = threading.Event()
running_threads['sron'] = threading.Event()

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