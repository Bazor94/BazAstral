import time
import test_config

def worker():
    while not test_config.stop_threads:
        print("Działam...")
        time.sleep(1)
    print("Kończę!")