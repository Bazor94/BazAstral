from EP import login
import logging
import threads


def refresh_cron():
    if not threads.running_threads['refresh'].is_set():
        return

    driver = login.login()

    refresh(driver)

    driver.quit()

@threads.stoper(threads.stop_threads, threads.running_threads['refresh'])
def refresh(driver):
    #delay = random.uniform(15*60, 30*60)  # refresh strony pomiedzy 15 a 30 min, zeby ewentualnie podmienic cookies
    delay = 7200
    threads.stop_threads.wait(delay)

    if not threads.stop_threads.is_set():
        login.refresh_and_set(driver)