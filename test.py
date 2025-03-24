import threading
import time
import test2
import test_config

thread = threading.Thread(target=test2.worker)
thread.start()

time.sleep(3)
test_config.stop_threads = True  # Modyfikacja zmiennej działa na cały program
thread.join()
