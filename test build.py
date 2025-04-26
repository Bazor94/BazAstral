from EP import login, planet, home, resources, empire
from models import models, calc
from services import fleet_service
import time
from datetime import datetime
from logger import logger


def get_transport_movement():
    missions = fleet_service.get_missions()['Transport']

    return missions


time_delay = 15


# login.login()
home.get_planets()
wanted_mines=models.Buildings(56, 52, 48)

main_planet = models.search_for_planet(models.planets, "3:147:8")
other_main_planet = models.search_for_planet(models.planets, "3:351:7")
other_planets = [p for p in models.planets if p != main_planet and p != other_main_planet]

other_planet_ids = [p.id for p in models.planets]
#fleet_service.gather_all_resources(main_planet.id, other_planet_ids, "LIGHT_CARGO")

missions = get_transport_movement()

max_time = 0
for m in missions:
    if m.arrive_date == None:
        continue

    total_seconds = int((m.arrive_date - datetime.now()).total_seconds())
    if total_seconds > max_time:
        max_time = total_seconds

time_sleep = max_time + time_delay
logger.sleep_log("building", main_planet, time_sleep, prefix="Gather | ")
#time.sleep(time_sleep)

emp = empire.get_empire_info(models.planets)


for p in models.planets:
    res_left, _ = resources.get_buildings_and_resources(main_planet)
    buildings = emp[p.coords]["buildings"]

    if buildings.metal_mine < wanted_mines.metal_mine:
        res_needed = calc.calculateMetalMineCost(buildings.metal_mine + 1)
        if res_needed < res_left:
            logger.info(f'Metal Mine | sending resources to {p}: {res_needed}', extra={"action": "building", "planet": main_planet})
            fleet_service.transport_resources(main_planet, False, p.x, p.y, p.z, False, res_needed)
            continue
        else:
            continue

    if buildings.crystal_mine < wanted_mines.crystal_mine:
        res_needed = calc.calculateCrystalMineCost(buildings.crystal_mine + 1)
        if res_needed < res_left:
            logger.info(f'Crystal Mine | sending resources to {p}: {res_needed}', extra={"action": "building", "planet": main_planet})
            fleet_service.transport_resources(main_planet, False, p.x, p.y, p.z, False, res_needed)
            continue
        else:
            continue

    if buildings.deuterium_refinery < wanted_mines.deuterium_refinery:
        res_needed = calc.calculateDeuteriumRefineryCost(buildings.deuterium_refinery + 1)
        if res_needed < res_left:
            logger.info(f'Deuterium Refinery | sending resources to {p}: {res_needed}', extra={"action": "building", "planet": main_planet})
            fleet_service.transport_resources(main_planet, False, p.x, p.y, p.z, False, res_needed)
            continue
        else:
            continue
