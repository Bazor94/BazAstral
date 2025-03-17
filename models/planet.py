import logging

planets = []

class Planet:
    def __init__(self, x: int, y: int, z: int, name: str, id: str, moon_id: str = None):
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        self.id = id 
        self.moon_id = moon_id  # ID księżyca, domyślnie None

    def __repr__(self):
        return f"Planet(x={self.x}, y={self.y}, z={self.z}, name={self.name}, id={self.id}, moon_id={self.moon_id})"
    
def search_for_planet(planets, coords):
    x, y, z = map(int, coords.split(':'))
    for planet in planets:
        if planet.x == x and planet.y == y and planet.z == z:
            return planet
        
    logging.ERROR(f"cannot find planet {coords}")
    return None
        