from EP import fleet
import time

mission_type_asteroid = "12"
mission_type_exp = "1"
mission_type_transport = "4"
planetTypePlanet = 1
planetTypeMoon = 2

def send_full_miners(x, y, from_planet_id):
    ships, referer_url = fleet.get_fleet(from_planet_id)
    time.sleep(1)
    miners = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] == 'ASTEROID_MINER']}
    fleet.send_fleet_2(miners, referer_url)
    time.sleep(1)
    fleet.send_fleet_3(miners, x, y, 17, referer_url)
    time.sleep(1)
    fleet.submit_fleet(miners, x, y, 17, mission_type_asteroid, 1, referer_url)

def send_full_miners_fs(x, y, z, from_planet_id):
    ships, referer_url = fleet.get_fleet(from_planet_id)
    time.sleep(1)
    miners = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] == 'ASTEROID_MINER']}
    fleet.send_fleet_2(miners, referer_url)
    time.sleep(1)
    fleet.send_fleet_3(miners, x, y, z, referer_url)
    time.sleep(1)
    fleet.submit_fleet(miners, x, y, z, mission_type_transport, 2, referer_url)

def transport_resources(x, y, z, metal, crystal, deuter):
    ships, referer_url = fleet.get_fleet()
    time.sleep(1)
    miners = {'Ships': [ship for ship in ships['Ships'] if ship['ShipType'] == 'ASTEROID_MINER']}
    fleet.send_fleet_2(miners, referer_url)
    time.sleep(1)
    fleet.send_fleet_3(miners, x, y, z, referer_url)
    time.sleep(1)
    fleet.submit_fleet(miners, x, y, z, mission_type_transport, 2, referer_url)
