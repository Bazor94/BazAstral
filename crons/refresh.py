from EP import login
import logging
import threads
from config import config


def refresh_cron():
    if not threads.running_threads['refresh'].is_set():
        return

    driver = login.login()

    refresh(driver)

    driver.quit()

@threads.stoper(threads.stop_threads, threads.running_threads['refresh'])
def refresh(driver):
    threads.stop_threads.wait(config.crons.refresh.interval)

    if not threads.stop_threads.is_set():
        login.refresh_and_set(driver)