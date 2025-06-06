from EP import fleet
import logging
import models.errors as errors
import threads
from models import models
import math

mission_type_asteroid = "12"
mission_type_exp = "1"
mission_type_transport = "4"
mission_type_deploy = "5"
mission_type_colonize = "2"
planetTypePlanet = 1
planetTypeMoon = 2


@threads.locker()
def send_full_miners(x, y, from_planet_id, percent_miners):
    ships, referer_url = fleet.get_fleet(from_planet_id)
    miners = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] == 'ASTEROID_MINER']} 
    if len(miners['Ships']) == 0:
        raise errors.ZeroShipsException("Zero miners")
    current_queantity = int(miners['Ships'][0]["Quantity"]) # TODO refactor
    miners['Ships'][0]["Quantity"] = str(int(current_queantity * (percent_miners / 100)))
    fleet.send_fleet_2(miners, referer_url)
    fleet.send_fleet_3(miners, x, y, 17, referer_url)
    fleet.submit_fleet(miners, x, y, 17, mission_type_asteroid, 1, None, referer_url)
    threads.refresh_missions_gui.put("refresh")


@threads.locker()
def send_full_miners_fs(x, y, z, from_planet_id, speed = 50):
    ships, referer_url = fleet.get_fleet(from_planet_id)
    miners = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] == 'ASTEROID_MINER']}
    fleet.send_fleet_2(miners, referer_url)
    fleet.send_fleet_3(miners, x, y, z, referer_url)
    fleet.submit_fleet(miners, x, y, z, mission_type_transport, 2, None, referer_url, speed)


@threads.locker()
def transport_resources(base_planet, is_from_moon, x, y, z, is_to_moon, resources: models.Resources):
    light_cargo_capacity=53000
    light_cargos_needed = math.ceil((resources.metal + resources.crystal + resources.deuterium) / light_cargo_capacity)

    base_planet_id = base_planet.moon_id if is_from_moon else base_planet.id

    ships, _, referer_url = fleet.get_fleet_and_resources(base_planet_id)
    cargo_ships = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] == 'LIGHT_CARGO']}
    if len(cargo_ships['Ships']) == 0:
        raise errors.NoShipsCustomException("zero cargo ships")
    
    if cargo_ships['Ships'][0]['Quantity'] < light_cargos_needed:
        raise errors.NoShipsCustomException("not enough cargo ships")
    
    cargo_ships['Ships'][0]['Quantity'] = light_cargos_needed
    
    fleet.send_fleet_2(cargo_ships, referer_url)
    resp = fleet.send_fleet_3(cargo_ships, x, y, z, referer_url)
    cargo_cap = resp["CargoCapacity"]

    if cargo_cap < resources.deuterium + resources.crystal + resources.metal:
        cargo_ships = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] in ['LIGHT_CARGO', 'HEAVY_CARGO']]}
        fleet.send_fleet_2(cargo_ships, referer_url)
        resp = fleet.send_fleet_3(cargo_ships, x, y, z, referer_url)
        cargo_cap = resp["CargoCapacity"]

    cargo = models.Resources(0, 0, 0)
    if cargo_cap < resources.deuterium:
        cargo.deuterium = cargo_cap
    elif cargo_cap < resources.deuterium + resources.crystal:
        cargo.deuterium = resources.deuterium
        cargo.crystal = cargo_cap - resources.deuterium
    elif cargo_cap < resources.deuterium + resources.crystal + resources.metal:
        cargo.deuterium = resources.deuterium
        cargo.crystal = resources.crystal
        cargo.metal = cargo_cap - resources.metal - resources.crystal
    else:
        cargo.deuterium = resources.deuterium
        cargo.crystal = resources.crystal
        cargo.metal = resources.metal

    moon_var = 2 if is_to_moon else 1
    fleet.submit_fleet(cargo_ships, x, y, z, mission_type_transport, moon_var, cargo, referer_url)


@threads.locker()
def send_expedition_with_resources(planet, hold_time_on_minutes=60):
    ships, resources, referer_url = fleet.get_fleet_and_resources(planet.moon_id)
    battle_ships = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] != 'ASTEROID_MINER']}
    if len(battle_ships['Ships']) == 0:
        raise errors.NoShipsCustomException("zero battle ships")
    
    fleet.send_fleet_2(battle_ships, referer_url)
    resp = fleet.send_fleet_3(battle_ships, planet.x, planet.y, 16, referer_url)
    cargo_cap = resp["CargoCapacity"]

    cargo = models.Resources(0, 0, 0)
    if cargo_cap < resources.deuterium:
        cargo.deuterium = cargo_cap
    elif cargo_cap < resources.deuterium + resources.crystal:
        cargo.deuterium = resources.deuterium
        cargo.crystal = cargo_cap - resources.deuterium
    elif cargo_cap < resources.deuterium + resources.crystal + resources.metal:
        cargo.deuterium = resources.deuterium
        cargo.crystal = resources.crystal
        cargo.metal = cargo_cap - resources.metal - resources.crystal
    else:
        cargo.deuterium = resources.deuterium
        cargo.crystal = resources.crystal
        cargo.metal = resources.metal

    fleet.submit_fleet(battle_ships, planet.x, planet.y, 16, mission_type_exp, 2, cargo, referer_url, hold_time_on_minutes=hold_time_on_minutes)



@threads.locker()
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
    fleet.submit_fleet(ships_dict, target_planet.x, target_planet.y, target_planet.z, mission_type_deploy, 2, None, referer_url)


def get_ships(ships, type):
    for ship in ships['Ships']:
        if ship['ShipType'] == type:
            return ship
        
    return None


@threads.locker()
def collect_all_resources(planet_id, planet_ids, ships):
    _, referer_url = fleet.get_fleet(planet_id)
    _, referer_url = fleet.get_collect_resources(planet_id, referer_url)
    fleet.collect_all_resources(planet_id, planet_ids, ships, referer_url)


@threads.locker()
def gather_all_resources(planet_id, planet_ids, ships):
    _, referer_url = fleet.get_fleet(planet_id)
    _, referer_url = fleet.get_gather_resources(planet_id, referer_url)
    fleet.gather_all_resources(planet_id, planet_ids, ships, referer_url)


@threads.locker()
def colonize_planet(x, y, z, from_planet_id):
    ships, referer_url = fleet.get_fleet(from_planet_id)
    colony_ship = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] == 'COLONY_SHIP']}
    colony_ship['Ships'][0]['Quantity'] = 1
    fleet.send_fleet_2(colony_ship, referer_url)
    fleet.send_fleet_3(colony_ship, x, y, z, referer_url)
    fleet.submit_fleet(colony_ship, x, y, z, mission_type_colonize, 1, None, referer_url)


@threads.locker()
def get_missions():
    fleet_movement, _ = fleet.get_feet_movement()
    
    missions = {}
    missions['Asteroid Mining'] = [mission for mission in fleet_movement if mission.mission_type in ['Asteroid Mining', 'Asteroid Mining (R)']]
    missions['Expedition'] = [mission for mission in fleet_movement if mission.mission_type in ['Expedition', 'Expedition (R)']]
    missions['Colonize'] = [mission for mission in fleet_movement if mission.mission_type in ['Colonize']]
    missions['Attack'] = [mission for mission in fleet_movement if mission.mission_type in ['Attack', 'Attack (R)']]
    missions['Transport'] = [mission for mission in fleet_movement if mission.mission_type in ['Transport', 'Transport (R)']]

    return missions


def update_missions():
    fleet_movement, _ = fleet.get_feet_movement()
    
    missions = {}
    for f in fleet_movement:
        mission_type = f.mission_type.split(' ')[0]

        if mission_type not in missions:
            missions[mission_type] = []
        
        missions[mission_type].append(f)

    models.missions = missions
