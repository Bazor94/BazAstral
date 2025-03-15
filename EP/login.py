from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
from webdriver_manager.chrome import ChromeDriverManager
import logging
import threading
import config
import helpers
import thread_lock

@thread_lock.locker(thread_lock.is_idle)
def login():
    print('login start')
    # Konfiguracja opcji dla Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")

    # Inicjalizacja WebDrivera
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Wejście na stronę
        url = "https://ogamex.net/"
        driver.get(url)
        time.sleep(2)  # Poczekaj na załadowanie strony

        # Kliknięcie w pierwszy przycisk "Login"
        login_button = driver.find_element(By.XPATH, "//a[contains(@onclick, 'OpenLogin()')]")
        driver.execute_script("arguments[0].click();", login_button)
        time.sleep(0.5)

        # Kliknięcie w drugi przycisk "Login"
        switch_login_button = driver.find_element(By.XPATH, "//a[contains(@onclick, 'SwitchToLogin()')]")
        driver.execute_script("arguments[0].click();", switch_login_button)
        time.sleep(0.5)

        # Wpisanie emaila
        email_input = driver.find_element(By.NAME, "Email")
        email_input.send_keys(config.login)

        # Wpisanie hasła
        password_input = driver.find_element(By.NAME, "Password")
        password_input.send_keys(config.password)

        # Kliknięcie w przycisk "Login"
        submit_button = driver.find_element(By.ID, "btnLogin")
        driver.execute_script("arguments[0].click();", submit_button)
        time.sleep(2)  # Poczekaj na zalogowanie

        # Kliknięcie w "Play" dla konkretnego serverId
        server_id = "099324e1-6ea9-442e-a7dd-29d66c9ddc79" # TODO zmienic to zeby bylo bardziej generyczne
        play_button = driver.find_element(By.XPATH, f"//a[contains(@href, '/connect?serverId={server_id}')]")
        driver.execute_script("arguments[0].click();", play_button)
        
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)  # Poczekaj na załadowanie gry

        # Pobranie ciasteczek po zalogowaniu
        cookies = driver.get_cookies()
        set_cookies(cookies)

        return driver 

    except Exception as e:
        driver.quit()
        raise Exception("Wystąpił błąd przy logowaniu")


@thread_lock.locker(thread_lock.is_idle)
def refresh(driver):
    driver.refresh()


def refresh_and_set(driver):
    logging.info("refreshing the page for cookies")
    refresh(driver)

    time.sleep(2)

    cookies = driver.get_cookies()
    set_cookies(cookies)


def refresh_cron(driver, stop_threads):
    while not stop_threads.is_set():
        #delay = random.uniform(15*60, 30*60)  # refresh strony pomiedzy 15 a 30 min, zeby ewentualnie podmienic cookies
        delay = 7200
        stop_threads.wait(delay)

        refresh_and_set(driver)

    driver.quit()


def set_cookies(cookies):
    cf_clearance = next((cookie['value'] for cookie in cookies if cookie['name'] == 'cf_clearance'), None)
    session_id = next((c['value'] for c in cookies if c['name'] == 'SessionId'), None)
    game_auth_token = next((c['value'] for c in cookies if c['name'] == 'gameAuthToken'), None)

    # logging.info(f'setting cookies: \ncf_clearance={cf_clearance} \nsession_id={session_id} \ngame_auth_token={game_auth_token}')

    config.cookies.update({
        "cf_clearance": cf_clearance,
        "SessionId": session_id,
        "gameAuthToken": game_auth_token
    })

    config.save_config(cf_clearance, session_id, game_auth_token)
    

