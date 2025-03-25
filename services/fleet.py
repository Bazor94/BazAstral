from EP import fleet
import logging
import models.errors as errors
import threads

mission_type_asteroid = "12"
mission_type_exp = "1"
mission_type_transport = "4"
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
def collect_all_resources(planet_id, planet_ids, ships):
    _, referer_url = fleet.get_fleet(planet_id)
    _, referer_url = fleet.get_collect_resources(planet_id, referer_url)
    fleet.collect_all_resources(planet_id, planet_ids, ships, referer_url)

@threads.locker(threads.is_idle)
def get_missions():
    fleet_movement, _ = fleet.get_feet_movement()
    
    missions = {}
    missions['Asteroid Mining'] = [mission for mission in fleet_movement if mission.mission_type in ['Asteroid Mining', 'Asteroid Mining (R)']]
    missions['Expedition'] = [mission for mission in fleet_movement if mission.mission_type in ['Expedition', 'Expedition (R)']]

    return missions
