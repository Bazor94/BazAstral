import tkinter as tk
from tkinter import ttk
from services import fleet
from datetime import datetime, timedelta
from EP import home
from models import planet
from collections import defaultdict
import main_loop

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tabbed App")
        self.geometry("1000x800")
        
        # Tworzenie zakładek
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        
        # Tworzenie ramek dla każdej zakładki
        self.home_tab = ttk.Frame(self.notebook)
        self.asteroid_tab = ttk.Frame(self.notebook)
        self.expedition_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        
        # Dodawanie ramek do notebooka
        self.notebook.add(self.home_tab, text="Home")
        self.notebook.add(self.asteroid_tab, text="Asteroid")
        self.notebook.add(self.expedition_tab, text="Expedition")
        self.notebook.add(self.settings_tab, text="Settings")
        
        # Sekcja Asteroid Mining w Home
        asteroid_mining_frame = ttk.LabelFrame(self.home_tab, text="Asteroid Mining")
        asteroid_mining_frame.pack(fill="x", padx=10, pady=5)
        
        self.asteroid_list = ttk.Treeview(asteroid_mining_frame, columns=("Planet", "Return Time", "Asteroid Coords"), show="headings")
        self.asteroid_list.heading("Planet", text="Planet")
        self.asteroid_list.heading("Return Time", text="Return Time")
        self.asteroid_list.heading("Asteroid Coords", text="Asteroid Coords")
        self.asteroid_list.pack(fill="both", padx=5, pady=5)
        
        # Sekcja Autoexpeditions w Home
        autoexpedition_frame = ttk.LabelFrame(self.home_tab, text="Autoexpeditions")
        autoexpedition_frame.pack(fill="x", padx=10, pady=5)

        self.autoexpedition_list = ttk.Treeview(autoexpedition_frame, columns=("Planet", "Return Time", "Expeditions"), show="headings")
        self.autoexpedition_list.heading("Planet", text="Planet")
        self.autoexpedition_list.heading("Return Time", text="Return Time")
        self.autoexpedition_list.heading("Expeditions", text="Expeditions")
        self.autoexpedition_list.pack(fill="both", padx=5, pady=5)


        # Mockowane dane Asteroid Mining
        planet.planets = home.get_planets()
        missions = fleet.get_missions()
        for mission in missions['Asteroid Mining']:
            item = (mission.planet.name, mission.back_date - datetime.now(), mission.target_coords)
            self.asteroid_list.insert("", "end", values=item)
            
        
        # Mockowane dane Autoexpeditions
        mock_data = [("Mars", "5:23", "3"), ("Venus", "8:12", "5"), ("Jupiter", "12:45", "2")]
        for item in mock_data:
            self.autoexpedition_list.insert("", "end", values=item)
        
        # Logi w zakładce Asteroid
        asteroid_log_frame = ttk.LabelFrame(self.asteroid_tab, text="Asteroid Logs")
        asteroid_log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.asteroid_log = tk.Text(asteroid_log_frame, height=10, wrap="word")
        self.asteroid_log.pack(fill="both", expand=True, padx=5, pady=5)
        self.asteroid_log.insert("end", "Asteroid mining log data...\nMock log entry 1\nMock log entry 2\n")
        
        # Logi w zakładce Expedition
        expedition_log_frame = ttk.LabelFrame(self.expedition_tab, text="Expedition Logs")
        expedition_log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.expedition_log = tk.Text(expedition_log_frame, height=10, wrap="word")
        self.expedition_log.pack(fill="both", expand=True, padx=5, pady=5)
        self.expedition_log.insert("end", "Expedition log data...\nMock log entry A\nMock log entry B\n")
        
        # Przykładowa zawartość zakładki Settings
        ttk.Label(self.settings_tab, text="Settings Panel").pack(pady=20)

        # Pobierz misje i zacznij aktualizować liczniki
        self.load_missions()
        self.refresh_view()

        self.after(1000, main_loop)

        

    def load_missions(self):
        """Ładuje misje do pamięci i ustawia początkowe wartości"""
        missions = fleet.get_missions()
        self.mission_data = {"Asteroid Mining": [], "Expedition": []}

        # Czyszczenie widoków
        for i in self.asteroid_list.get_children():
            self.asteroid_list.delete(i)
        for i in self.autoexpedition_list.get_children():
            self.autoexpedition_list.delete(i)

        # Przetwarzanie Asteroid Mining
        for mission in missions.get("Asteroid Mining", []):
            time_remaining = (mission.back_date - datetime.now()).total_seconds()
            self.mission_data["Asteroid Mining"].append([mission.planet.name + f" {mission.planet.coords}", time_remaining, mission.target_coords])

        # Przetwarzanie Autoexpeditions
        expeditions_num = defaultdict(int)
        for mission in missions.get("Expedition", []):
            expeditions_num[mission.planet.coords] += 1

        for mission in missions.get("Expedition", []):
            time_remaining = (mission.back_date - datetime.now()).total_seconds()
            self.mission_data["Expedition"].append([mission.planet.name + f" {mission.planet.coords}", time_remaining, expeditions_num[mission.planet.coords]])


    def refresh_view(self):
        """Odświeża wyświetlanie danych"""
        for category in ["Asteroid Mining", "Expedition"]:
            for mission in self.mission_data[category]:
                if mission[1] > 0:
                    mission[1] -= 1  # Odejmujemy 1 sekundę
                else:
                    mission[1] = "done"

        # Czyszczenie tabel
        for i in self.asteroid_list.get_children():
            self.asteroid_list.delete(i)
        for i in self.autoexpedition_list.get_children():
            self.autoexpedition_list.delete(i)

        # Wypełnianie tabel
        for mission in self.mission_data["Asteroid Mining"]:
            formatted_time = mission[1] if mission[1] == "done" else str(timedelta(seconds=int(mission[1])))
            self.asteroid_list.insert("", "end", values=(mission[0], formatted_time, mission[2]))

        for mission in self.mission_data["Expedition"]:
            formatted_time = mission[1] if mission[1] == "done" else str(timedelta(seconds=int(mission[1])))
            self.autoexpedition_list.insert("", "end", values=(mission[0], formatted_time, mission[2]))

        self.after(1000, self.refresh_view)  # Odśwież co sekundę


if __name__ == "__main__":
    app = App()
    app.mainloop()
    main_loop.run_crons()


