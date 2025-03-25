from models import planet

class Mission:
    def __init__(self, arrive_date, back_date, mission_type: str, coords_from: str, coords_to: str):
        self.arrive_date = arrive_date
        self.back_date = back_date
        self.planet = planet.search_for_planet(planet.planets, coords_from)
        self.target_coords = coords_to

        self.mission_type = mission_type
