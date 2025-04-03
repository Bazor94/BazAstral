from logger import logger

planets = []

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
        