import requests
import config
from EP.home import get_planets  # Import funkcji get_planets
from EP.defense import create_defense  # Import funkcji create_defense

# Koszt budowy jednostek obrony (od najdroższych do najtańszych)
DEFENSE_COSTS = [
    {"type": "OrbitalDefensePlatform", "metal": 128000000, "crystal": 96000000, "deuterium": 24000000},
    {"type": "DoomCannon", "metal": 20000000, "crystal": 16000000, "deuterium": 2000000},
    {"type": "Fortress", "metal": 2400000, "crystal": 2400000, "deuterium": 400000},
    {"type": "AtmosphericShield", "metal": 20000000, "crystal": 20000000, "deuterium": 10000000},
    {"type": "LargeShieldDome", "metal": 100000, "crystal": 100000, "deuterium": 0},
    {"type": "SmallShieldDome", "metal": 20000, "crystal": 20000, "deuterium": 0}
]

def build_defenses_on_all_planets():
    # Pobierz listę planet
    planets = get_planets()

    for planet in planets:
        planet_id = planet.id
        print(f"Przetwarzanie planety: {planet.name} (ID: {planet_id})")

        # Budowanie jednostek obrony od najdroższych do najtańszych
        for defense in DEFENSE_COSTS:
            defense_type = defense["type"]

            # Próbuj budować jednostki, aż nie uda się zbudować kolejnej
            while True:
                try:
                    print(f"Próba budowania 1 {defense_type}...")
                    create_defense(planet_id, defense_type, 1)  # Buduj 1 jednostkę
                except Exception as e:
                    print(f"Nie udało się zbudować {defense_type}: {e}")
                    break  # Przerwij, jeśli nie udało się zbudować jednostki

        print(f"Zakończono budowanie obrony na planecie {planet.name}.\n")

if __name__ == "__main__":
    build_defenses_on_all_planets()