import http_requester as requests
import config
from bs4 import BeautifulSoup

class Defense:
    def __init__(self):
        # Definicja wszystkich elementów obrony
        self.missile_launcher = self.DefenseUnit("MISSILE_LAUNCHER")
        self.light_laser_turret = self.DefenseUnit("LIGHT_LASER_TURRET")
        self.heavy_laser_turret = self.DefenseUnit("HEAVY_LASER_TURRET")
        self.ion_cannon = self.DefenseUnit("ION_CANNON")
        self.gauss_cannon = self.DefenseUnit("GAUSS_CANNON")
        self.plasma_cannon = self.DefenseUnit("PLASMA_CANNON")
        self.dora_gun = self.DefenseUnit("DORA_GUN")
        self.photon_cannon = self.DefenseUnit("PHOTON_CANNON")
        self.interceptor = self.DefenseUnit("INTERCEPTOR")
        self.interplanetary_missile = self.DefenseUnit("INTERPLANETARY_MISSILE")

        # Platformy obronne
        self.fortress = self.DefenseUnit("FORTRESS")
        self.doom_cannon = self.DefenseUnit("DOOM_CANNON")
        self.orbital_defense_platform = self.DefenseUnit("ORBITAL_DEFENSE_PLATFORM")

        # Tarcze ochronne
        self.small_shield_dome = self.DefenseUnit("SMALL_SHIELD_DOME")
        self.large_shield_dome = self.DefenseUnit("LARGE_SHIELD_DOME")
        self.atmospheric_shield = self.DefenseUnit("ATMOSPHERIC_SHIELD")

    def set_values(self, name, quantity, max_value, metal_needed, crystal_needed, deuterium_needed):
        attr_name = name.lower().replace(" ", "_")
        if hasattr(self, attr_name):
            unit = getattr(self, attr_name)
            unit.quantity = quantity
            unit.max = max_value
            unit.metal = metal_needed
            unit.crystal = crystal_needed
            unit.deuterium = deuterium_needed

    class DefenseUnit:
        def __init__(self, name, quantity=0, max_value=None):
            self.quantity = quantity
            self.max = max_value
            self.name = name
        def get_name(self):
            return self.name

def get_defense(planet_id) -> Defense:
    url = f"{config.host}/defense"
    headers = {**config.headers, "referer": f"{config.host}/home" }

    params = {
        "planet": planet_id
    }

    response = requests.get(url, headers=headers, cookies=config.cookies, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    defense = Defense()
    for item in soup.find_all("div", class_="hangar-detail"):
        title_tag = item.find("h3", class_="hangar-title")
        name = title_tag.text.strip()

        metal_needed = int(item.find("span", class_="x-resource-metal").text.replace(".", ""))
        try:
            crystal_needed = int(item.find("span", class_="x-resource-crystal").text.replace(".", ""))
        except:
            crystal_needed = None

        try:
            deuterium_needed = int(item.find("span", class_="x-resource-deuterium").text.replace(".", ""))
        except:
            deuterium_needed = None
        
        level_tag = item.find("h3", class_="hangar-level")
        level_text = level_tag.text.replace("Available:", "").replace(".", "").strip()

        if "/" in level_text:
            quantity, max_value = level_text.split(" / ")
            quantity = int(quantity)
            max_value = int(max_value)
        else:
            quantity = int(level_text)
            max_value = None

        defense.set_values(name, quantity, max_value, metal_needed, crystal_needed, deuterium_needed)

    metal = int(soup.find("span", id="metal-amount").text.replace(".", ""))
    crystal = int(soup.find("span", id="crystal-amount").text.replace(".", ""))
    deuterium = int(soup.find("span", id="deuterium-amount").text.replace(".", ""))
    resources = {"metal": metal, "crystal": crystal, "deuterium": deuterium}

    return defense, resources, response.url

def create_defense(planet_id, name, quantity, referer_url):
    url = f"{config.host}/defense/createdefense"
    headers = {**config.headers, "referer": referer_url }

    data = {
        "Quantity": quantity,
        "DefenseType": name,
        "__PlanetId": planet_id
    }

    response = requests.post(url, headers=headers, cookies=config.cookies, json=data)

    return response.text
