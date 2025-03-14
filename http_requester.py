import time
import random
import requests
import logging
import config
from bs4 import BeautifulSoup
import json
import errors


def get(url, params=None, **kwargs):
    headers = kwargs.get("headers", {}) 
    cookies = kwargs.get("cookies", {})
    response = requests.get(url, headers=headers, cookies=cookies, params=params)

    if response.status_code != 200:
        logging.warning(f"{url} with params: {params} and kwargs {kwargs} returned status code {response.status_code}")
        raise ValueError(f"{url} status code is not 200")

    soup = BeautifulSoup(response.text, 'html.parser')
    captcha = soup.find("div", class_="g-recaptcha")

    if captcha:
        logging.warning(f"{url} with params: {params} and kwargs {kwargs} returned captcha")
        raise ValueError(f"{url} captcha appeared")

    without_sleep = kwargs.pop("without_sleep", False)
    if not without_sleep:
        time.sleep(random.uniform(0.5, 0.75))

    return response

def post(url, params=None, **kwargs):
    headers = kwargs.get("headers", {}) 
    cookies = kwargs.get("cookies", {})
    data = kwargs.get("json", {})
    response = requests.post(url, headers=headers, cookies=cookies, params=params, json=data)

    if response.status_code != 200:
        logging.warning(f"{url} with params: {params} and kwargs {kwargs} returned status code {response.status_code}")
        raise ValueError(f"{url} status code is not 200")

    soup = BeautifulSoup(response.text, 'html.parser')
    captcha = soup.find("div", class_="g-recaptcha")

    if captcha:
        logging.warning(f"{url} with params: {params} and kwargs {kwargs} returned captcha")
        raise ValueError(f"{url} captcha appeared")
    
    try:
        bodyData = json.loads(response.text)
        is_success = bodyData.get("IsSuccess")
        message = bodyData.get("Message")
        validation_errors = bodyData.get("ValidationErrors")

        if is_success is False:
            if message == errors.wrongPlanetMessage:
                raise errors.WrongPlanetException(f"Wrong Planet - {url} IsSuccess is false")
            elif message == errors.notEnoughResourcesMessage:
                raise errors.NotEnoughResourcesException(f"Not enought resources - {url} IsSuccess is false")
            elif message == errors.maximumLimitMessage:
                raise errors.MaximumLimitException(f"Limit reached - {url} IsSuccess is false")
            elif message == errors.shipsNotFoundMessage:
                raise errors.ShipsNotFoundException(f"Ships not found - {url} IsSuccess is false")
            elif message == errors.notEnoughDeuterium:
                raise errors.NotEnoughDeuterium(f"Not enought deuterium - {url} IsSuccess is false")
            elif message == errors.notEnoughShipsMessage:
                raise errors.NotEnoughShipsException(f"Not enough ships - {url} IsSuccess is false")
            else:
                raise ValueError(f"Unexpected error - {url} IsSuccess is false")
    except json.JSONDecodeError:
        logging.warning(f"{url} with params: {params} and kwargs {kwargs} cannot decode json: {bodyData}")
        raise ValueError(f"{url} cannot decode json")

    without_sleep = kwargs.pop("without_sleep", False)
    if not without_sleep:
        time.sleep(random.uniform(0.5, 0.75))

    return response