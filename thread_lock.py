import threading

is_idle = threading.Event()
is_idle.set()

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