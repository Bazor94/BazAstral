from EP import login, planet, home, resources, empire
from models import models, calc
import time
from logger import logger
import threading
import threads


def building_on_planets_cron(p):
    while True:
        build_mine(p)


@threads.locker()
def build(p, building):
    _, _, referer_url = resources.get_buildings_and_resources(p)
    resources.increase_building(p, building, referer_url)


        
def build_mine(p):
    planet_empire = emp[p.coords]

    metal_mine = planet_empire["buildings"].metal
    crystal_mine = planet_empire["buildings"].crystal
    deuterium_refinery = planet_empire["buildings"].deuterium

    _, res, _ = resources.get_buildings_and_resources(p)

    if metal_mine <= crystal_mine + 2:
        cost = calc.calculateMetalMineCost(metal_mine)

        remaining_metal = res.metal - cost.metal
        remaining_crystal = res.crystal - cost.crystal

        time_sleep = 0
        if remaining_metal < 0:
            time_sleep = remaining_metal / planet_empire["production"].metal * -3600
        if remaining_crystal < 0:
            time_needed = remaining_crystal / planet_empire["production"].crystal * -3600
            if time_needed > time_sleep:
                time_sleep = time_needed

        if time_sleep > 0:
            time_sleep = int(time_sleep)
            logger.sleep_log("building", p, time_sleep, prefix="Metal Mine | ")
            time.sleep(time_sleep)
        
        try:
            logger.info("building Metal Mine", extra={"planet": p, "action": "building"})
            build(p, "METAL_MINE")
            planet_empire["buildings"].metal += 1
        except Exception as e:
            logger.warning(e)
            time.sleep(5*60)

        return

    elif crystal_mine <= deuterium_refinery + 7:
        cost = calc.calculateCrystalMineCost(crystal_mine)

        remaining_metal = res.metal - cost.metal
        remaining_crystal = res.crystal - cost.crystal

        time_sleep = 0
        if remaining_metal < 0:
            time_sleep = remaining_metal / planet_empire["production"].metal * -3600
        if remaining_crystal < 0:
            time_needed = remaining_crystal / planet_empire["production"].crystal * -3600
            if time_needed > time_sleep:
                time_sleep = time_needed

        if time_sleep > 0:
            time_sleep = int(time_sleep)
            logger.sleep_log("building", p, time_sleep, prefix="Crystal Mine | ")
            time.sleep(time_sleep)
        
        try:
            logger.info("building Crystal Mine", extra={"planet": p, "action": "building"})
            build(p, "CRYSTAL_MINE")
            planet_empire["buildings"].crystal += 1
        except Exception as e:
            logger.warning(e)
            time.sleep(5*60)

        return
    else:
        cost = calc.calculateDeuteriumRefineryCost(crystal_mine)

        remaining_metal = res.metal - cost.metal
        remaining_crystal = res.crystal - cost.crystal

        time_sleep = 0
        if remaining_metal < 0:
            time_sleep = remaining_metal / planet_empire["production"].metal * -3600
        if remaining_crystal < 0:
            time_needed = remaining_crystal / planet_empire["production"].crystal * -3600
            if time_needed > time_sleep:
                time_sleep = time_needed

        if time_sleep > 0:
            time_sleep = int(time_sleep)
            logger.sleep_log("building", p, time_sleep, prefix="Deuterium Refinery | ")
            time.sleep(time_sleep)
        
        try:
            logger.info("building Deuterium Refinery", extra={"planet": p, "action": "building"})
            build(p, "DEUTERIUM_REFINERY")
            planet_empire["buildings"].deuterium += 1
        except Exception as e:
            logger.warning(e)
            time.sleep(5*60)

        return


def refresh_empire():
    while True:
        time.sleep(5*60)
        global emp
        emp = empire.get_empire_info(models.planets)


# login.login()
home.get_planets()
emp = empire.get_empire_info(models.planets)


threads_list = []
for p in models.planets:
    threads_list.append(threading.Thread(target=building_on_planets_cron, args=(p, )))

threads_list.append(threading.Thread(target=refresh_empire))

for t in threads_list:
    t.start()

