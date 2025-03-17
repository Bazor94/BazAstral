import time
import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


while True:
    resp = requests.get('https://google.com')
    logging.info(f'{resp}')
    time.sleep(1)