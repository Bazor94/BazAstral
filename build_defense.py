from EP import defense
import logging
import errors
import time

def build_max_platforms_all_planets(planets):
    for planet in planets:
        logging.info(f'starting building defense on {planet.name}')
        buildings, _, referer_url = defense.get_defense(planet.id)

        wanted_buildings = ["orbital_defense_platform", "doom_cannon", "fortress", "small_shield_dome", "large_shield_dome", "atmospheric_shield"]

        for wanted_building in wanted_buildings:
            quantity = getattr(buildings, wanted_building).max - getattr(buildings, wanted_building).quantity
            try:
                defense.create_defense(planet.id, wanted_building.upper(), quantity, referer_url)
            except Exception as e:
                logging.warning(f'error building {quantity} {wanted_building} on {planet.name}: {e}')
                continue

def build_max_defense_one_planet(planet):
    logging.info(f'starting building defense on {planet.name}')
    buildings, resources, referer_url = defense.get_defense(planet.id)

    wanted_buildings = ["photon_cannon"]

    for wanted_building in wanted_buildings:
        max_quantity_metal =  int(resources['metal'] / getattr(buildings, wanted_building).metal)
        max_quantity_crystal =  int(resources['metal'] / getattr(buildings, wanted_building).crystal)
        max_quantity_deuterium =  int(resources['metal'] / getattr(buildings, wanted_building).deuterium)

        quantity = min(max_quantity_metal, max_quantity_crystal, max_quantity_deuterium)
        try:
            defense.create_defense(planet.id, wanted_building.upper(), quantity, referer_url)
        except Exception as e:
            logging.warning(f'error building {quantity} {wanted_building} on {planet.name}: {e}')
            continue

def build_def_cron(planet, seconds_delay, stop_threads):
    stop_threads.wait(5*60)

    while not stop_threads.is_set():
        build_max_defense_one_planet(planet)
        logging.info(f'building defence | sleeping for {seconds_delay}')
        stop_threads.wait(seconds_delay)