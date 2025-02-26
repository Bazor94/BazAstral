from EP import fleet

mission_type_asteroid = "12"
mission_type_exp = "1"

def send_full_miners(x, y, z):
    ships = fleet.get_fleet()
    miners = {'Ships': [ship for ship in ships[0]['Ships'] if ship['ShipType'] == 'ASTEROID_MINER']}
    fleet.send_fleet_2(miners)
    fleet.send_fleet_3(miners, x, y, 17)
    fleet.submit_fleet(miners, x, y, 17, mission_type_asteroid, 1)
