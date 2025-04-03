from EP import fleet
import logging
import models.errors as errors
import threads

mission_type_asteroid = "12"
mission_type_exp = "1"
mission_type_transport = "4"
mission_type_deploy = "5"
mission_type_colonize = "2"
planetTypePlanet = 1
planetTypeMoon = 2


@threads.locker(threads.is_idle)
def send_full_miners(x, y, from_planet_id, percent_miners):
    ships, referer_url = fleet.get_fleet(from_planet_id)
    miners = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] == 'ASTEROID_MINER']} 
    if len(miners['Ships']) == 0:
        raise errors.ZeroShipsException("Zero miners")
    current_queantity = int(miners['Ships'][0]["Quantity"]) # TODO refactor
    miners['Ships'][0]["Quantity"] = str(int(current_queantity * (percent_miners / 100)))
    fleet.send_fleet_2(miners, referer_url)
    fleet.send_fleet_3(miners, x, y, 17, referer_url)
    fleet.submit_fleet(miners, x, y, 17, mission_type_asteroid, 1, referer_url)
    threads.refresh_missions_gui.put("refresh")


@threads.locker(threads.is_idle)
def send_full_miners_fs(x, y, z, from_planet_id, speed = 50):
    ships, referer_url = fleet.get_fleet(from_planet_id)
    miners = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] == 'ASTEROID_MINER']}
    fleet.send_fleet_2(miners, referer_url)
    fleet.send_fleet_3(miners, x, y, z, referer_url)
    fleet.submit_fleet(miners, x, y, z, mission_type_transport, 2, referer_url, speed)


@threads.locker(threads.is_idle)
def transport_resources(x, y, z, metal, crystal, deuter): # TODO not working yet
    ships, referer_url = fleet.get_fleet()
    miners = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] == 'ASTEROID_MINER']}
    fleet.send_fleet_2(miners, referer_url)
    fleet.send_fleet_3(miners, x, y, z, referer_url)
    fleet.submit_fleet(miners, x, y, z, mission_type_transport, 2, referer_url)


@threads.locker(threads.is_idle)
def send_expedition_with_resources(planet):
    ships, referer_url = fleet.get_fleet()
    battle_ships = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] != 'ASTEROID_MINER']}
    fleet.send_fleet_2(battle_ships, referer_url)
    resp = fleet.send_fleet_3(battle_ships, planet.x, planet.y, 16, referer_url)
    cargo = resp["CargoCapacity"]

    fleet.submit_fleet(battle_ships, planet.x, planet.y, 16, mission_type_exp, 2, referer_url)


@threads.locker(threads.is_idle)
def deploy_ships(planet, target_planet, ships):
    planet_ships, referer_url = fleet.get_fleet(planet.moon_id)

    for ship in ships:
        planet_ship = get_ships(planet_ships, ship['ShipType'])
        if planet_ship is None:
            return False
        
        if planet_ship['Quantity'] < ship['Quantity']:
            return False

    ships_dict = {'Ships': ships}
    fleet.send_fleet_2(ships_dict, referer_url)
    fleet.send_fleet_3(ships_dict, target_planet.x, target_planet.y, target_planet.z, referer_url)
    fleet.submit_fleet(ships_dict, target_planet.x, target_planet.y, target_planet.z, mission_type_deploy, 2, referer_url)


def get_ships(ships, type):
    for ship in ships['Ships']:
        if ship['ShipType'] == type:
            return ship
        
    return None


@threads.locker(threads.is_idle)
def collect_all_resources(planet_id, planet_ids, ships):
    _, referer_url = fleet.get_fleet(planet_id)
    _, referer_url = fleet.get_collect_resources(planet_id, referer_url)
    fleet.collect_all_resources(planet_id, planet_ids, ships, referer_url)


@threads.locker(threads.is_idle)
def colonize_planet(x, y, z, from_planet_id):
    ships, referer_url = fleet.get_fleet(from_planet_id)
    colony_ship = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] == 'COLONY_SHIP']}
    colony_ship['Ships'][0]['Quantity'] = 1
    fleet.send_fleet_2(colony_ship, referer_url)
    fleet.send_fleet_3(colony_ship, x, y, z, referer_url)
    fleet.submit_fleet(colony_ship, x, y, z, mission_type_colonize, 1, referer_url)


@threads.locker(threads.is_idle)
def get_missions():
    fleet_movement, _ = fleet.get_feet_movement()
    
    missions = {}
    missions['Asteroid Mining'] = [mission for mission in fleet_movement if mission.mission_type in ['Asteroid Mining', 'Asteroid Mining (R)']]
    missions['Expedition'] = [mission for mission in fleet_movement if mission.mission_type in ['Expedition', 'Expedition (R)']]
    missions['Colonize'] = [mission for mission in fleet_movement if mission.mission_type in ['Colonize']]
    missions['Attack'] = [mission for mission in fleet_movement if mission.mission_type in ['Attack', 'Attack (R)']]

    return missions
