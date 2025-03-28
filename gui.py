import tkinter as tk
from tkinter import ttk
import threads
from services import fleet
from datetime import datetime, timedelta
from EP import home
from models import planet
from collections import defaultdict
import main_loop
import threading
from config import config, save_config
import logger
import logging
import ctypes
import queue


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tabbed App")

        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

        window_height = 700
        window_width = 1200

        position_top = int(screen_height/2 - window_height/2)
        position_right = int(screen_width/2 - window_width/2)

        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        
        # Tworzenie zakładek
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        
        # Tworzenie ramek dla każdej zakładki
        self.home_tab = ttk.Frame(self.notebook)
        self.asteroid_tab = ttk.Frame(self.notebook)
        self.expedition_tab = ttk.Frame(self.notebook)
        self.general_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        
        # Dodawanie ramek do notebooka
        self.notebook.add(self.home_tab, text="Home")
        self.notebook.add(self.asteroid_tab, text="Asteroid")
        self.notebook.add(self.expedition_tab, text="Expedition")
        self.notebook.add(self.general_tab, text="General")
        self.notebook.add(self.settings_tab, text="Settings")
        
        # Sekcja Asteroid Mining w Home
        asteroid_mining_frame = ttk.LabelFrame(self.home_tab, text="Asteroid Mining")
        asteroid_mining_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self.asteroid_list = ttk.Treeview(asteroid_mining_frame, columns=("Planet", "Return Time", "Asteroid Coords"), show="headings", height=15)
        self.asteroid_list.heading("Planet", text="Planet")
        self.asteroid_list.heading("Return Time", text="Return Time")
        self.asteroid_list.heading("Asteroid Coords", text="Asteroid Coords")
        self.asteroid_list.pack(fill="both", padx=5, pady=5)

        self.asteroid_checkbox_var = tk.BooleanVar(value=threads.running_threads['asteroid'].is_set())
        self.asteroid_checkbox = ttk.Checkbutton(
            asteroid_mining_frame, 
            text="Enable Asteroid Mining", 
            variable=self.asteroid_checkbox_var, 
            command=self.toggle_asteroid
        )
        self.asteroid_checkbox.pack(anchor="w", padx=5, pady=5)

        # Sekcja Autoexpeditions w Home
        autoexpedition_frame = ttk.LabelFrame(self.home_tab, text="Autoexpeditions")
        autoexpedition_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        self.autoexpedition_list = ttk.Treeview(autoexpedition_frame, columns=("Planet", "Return Time", "Expeditions"), show="headings", height=15)
        self.autoexpedition_list.heading("Planet", text="Planet")
        self.autoexpedition_list.heading("Return Time", text="Return Time")
        self.autoexpedition_list.heading("Expeditions", text="Expeditions")
        self.autoexpedition_list.pack(fill="both", padx=5, pady=5)

        self.expedition_checkbox_var = tk.BooleanVar(value=threads.running_threads['expedition'].is_set())
        self.expedition_checkbox = ttk.Checkbutton(
            autoexpedition_frame, 
            text="Enable Autoexpedition", 
            variable=self.expedition_checkbox_var, 
            command=self.toggle_autoexpedition
        )
        self.expedition_checkbox.pack(anchor="w", padx=5, pady=5)

        # Rozciąganie kolumn
        self.home_tab.columnconfigure(0, weight=1)
        self.home_tab.columnconfigure(1, weight=1)

        # Dane Asteroid Mining i Expeditions
        planet.planets = home.get_planets()
        missions = fleet.get_missions()
        for mission in missions['Asteroid Mining']:
            item = (mission.planet.name, mission.back_date - datetime.now(), mission.target_coords)
            self.asteroid_list.insert("", "end", values=item)
        
        # Logi w zakładce Asteroid
        asteroid_log_frame = ttk.LabelFrame(self.asteroid_tab, text="Asteroid Logs")
        asteroid_log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.asteroid_log = tk.Text(asteroid_log_frame, height=10, wrap="word")
        self.asteroid_log.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Logi w zakładce Expedition
        expedition_log_frame = ttk.LabelFrame(self.expedition_tab, text="Expedition Logs")
        expedition_log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.expedition_log = tk.Text(expedition_log_frame, height=10, wrap="word")
        self.expedition_log.pack(fill="both", expand=True, padx=5, pady=5)

        # Logi w zakładce Expedition
        general_log_frame = ttk.LabelFrame(self.general_tab, text="Expedition Logs")
        general_log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.general_log = tk.Text(general_log_frame, height=10, wrap="word")
        self.general_log.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Przykładowa zawartość zakładki Settings
        ttk.Label(self.settings_tab, text="Settings Panel").pack(pady=20)

        widget_handler = logger.WidgetHandler(self.asteroid_log, self.expedition_log, self.general_log)
        widget_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(action)s | %(planet)s | %(message)s'))
        logger.logger.addHandler(widget_handler)

        # Pobierz misje i zacznij aktualizować liczniki
        self.load_missions()
        self.refresh_view()


    def toggle_autoexpedition(self):
        if self.expedition_checkbox_var.get():
            threads.running_threads['expedition'].set()
            config.crons.expedition.enabled = True
            save_config()
        else:
            threads.running_threads['expedition'].clear()
            config.crons.expedition.enabled = False
            save_config()


    def toggle_asteroid(self):
        if self.asteroid_checkbox_var.get():
            threads.running_threads['asteroid'].set()
            config.crons.asteroid.enabled = True
            save_config()
        else:
            threads.running_threads['asteroid'].clear()
            config.crons.asteroid.enabled = False
            save_config()


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
        try:
            threads.refresh_missions_gui.get_nowait()
            self.load_missions()
        except queue.Empty:
            pass

        while not threads.refresh_missions_gui.empty(): # clear queue
             threads.refresh_missions_gui.get()

        for category in ["Asteroid Mining", "Expedition"]:
            for mission in self.mission_data[category]:
                if mission[1] != "done" and mission[1] > 0:
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

    threading.Thread(target=main_loop.run_crons, daemon=True).start()
    app.mainloop()
