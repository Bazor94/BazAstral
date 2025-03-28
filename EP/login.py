from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
from webdriver_manager.chrome import ChromeDriverManager
import logging
import threading
from config import config, save_config, cookies
import helpers
import threads

@threads.locker(threads.is_idle)
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
        email_input.send_keys(config.creds.login)

        # Wpisanie hasła
        password_input = driver.find_element(By.NAME, "Password")
        password_input.send_keys(config.creds.password)

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


@threads.locker(threads.is_idle)
def refresh(driver):
    driver.refresh()


def refresh_and_set(driver):
    logging.info("refreshing the page for cookies")
    refresh(driver)

    time.sleep(2)

    cookies = driver.get_cookies()
    set_cookies(cookies)


def set_cookies(cookies_list):
    cf_clearance = next((cookie['value'] for cookie in cookies_list if cookie['name'] == 'cf_clearance'), None)
    session_id = next((c['value'] for c in cookies_list if c['name'] == 'SessionId'), None)
    game_auth_token = next((c['value'] for c in cookies_list if c['name'] == 'gameAuthToken'), None)

    cookies.update({
        "cf_clearance": cf_clearance,
        "SessionId": session_id,
        "gameAuthToken": game_auth_token
    })

    save_config()
    

