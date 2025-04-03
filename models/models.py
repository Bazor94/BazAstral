expeditionType = 'Expedition'
expeditionReturnType = 'Expedition (R)'


missions = {}
planets = []


class Mission:
    def __init__(self, arrive_date, back_date, mission_type: str, coords_from: str, coords_to: str):
        self.arrive_date = arrive_date
        self.back_date = back_date
        self.planet = search_for_planet(planets, coords_from)
        self.target_coords = coords_to

        self.mission_type = mission_type

    def __repr__(self):
        return f"{self.mission_type}: [{self.planet}]->[{self.target_coords}]: ({self.arrive_date} | {self.back_date}))"


def getExpeditionMissions():
    return missions[expeditionType] + missions[expeditionReturnType]


class Planet:
    def __init__(self, coords: str, x: int, y: int, z: int, name: str, id: str, moon_id: str = None):
        self.x = x
        self.y = y
        self.z = z
        self.coords = coords
        self.name = name
        self.id = id
        self.moon_id = moon_id  # ID księżyca, domyślnie None

    def __repr__(self):
        return f"{self.name} {self.coords}" # uzywane do formatowania logow


def search_for_planet(planets, coords):
    x, y, z = map(int, coords.split(':'))
    for planet in planets:
        if planet.x == x and planet.y == y and planet.z == z:
            return planet

    return None


class Resources:
    def __init__(self, metal, crystal, deuterium):
        self.metal = metal
        self.crystal = crystal
        self.deuterium = deuterium
    

class PlanetEmpire:
    def __init__(self, planet):
        self.planet = planet
    
    def set_resources(self, resources: Resources):
        self.resources = resources

    def set_moon_resources(self, resources: Resources):
        self.moon_resources = resources


class Empire:
    def __init__(self, planet_empires):
        self.planet_empires = planet_empires