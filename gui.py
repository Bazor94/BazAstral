import tkinter as tk
from tkinter import ttk
from models import models
import threads
from services import fleet_service
from datetime import datetime, timedelta
from EP import home
from collections import defaultdict
import main_loop
import threading
from config import config, save_config
import logger
import logging
import ctypes
import queue
from services import colonize_planet


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
        self.functions_tab = ttk.Frame(self.notebook)
        self.logs_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        
        # Dodawanie ramek do notebooka
        self.notebook.add(self.home_tab, text="Home")
        self.notebook.add(self.functions_tab, text="Functions")
        self.notebook.add(self.logs_tab, text="Logs")
        self.notebook.add(self.settings_tab, text="Settings")
        
        # ------------------------------------------
        # -------------- HOME ----------------------
        # ------------------------------------------
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
        models.planets = home.get_planets()
        missions = fleet_service.get_missions()
        for mission in missions['Asteroid Mining']:
            item = (mission.planet.name, mission.back_date - datetime.now(), mission.target_coords)
            self.asteroid_list.insert("", "end", values=item)
        

        # Sekcja general
        general_frame = ttk.LabelFrame(self.home_tab, text="General")
        general_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.plunder_checkbox_var = tk.BooleanVar(value=threads.running_threads['plunder'].is_set())
        self.plunder_checkbox = ttk.Checkbutton(
            general_frame, 
            text="Enable Plunder", 
            variable=self.plunder_checkbox_var, 
            command=self.toggle_plunder
        )
        self.plunder_checkbox.pack(anchor="w", padx=5, pady=5)


        # Sekcja Funkcji
        colonize_frame = ttk.LabelFrame(self.functions_tab, text="Colonize")
        colonize_frame.pack(fill="x", padx=10, pady=5)

        # Pole "Coords From"
        ttk.Label(colonize_frame, text="Coords From:").grid(row=0, column=0, padx=5, pady=5)
        self.coords_from_entry = ttk.Entry(colonize_frame)
        self.coords_from_entry.grid(row=0, column=1, padx=5, pady=5)

        # Pole "Coords To"
        ttk.Label(colonize_frame, text="Coords To:").grid(row=0, column=2, padx=5, pady=5)
        self.coords_to_entry = ttk.Entry(colonize_frame)
        self.coords_to_entry.grid(row=0, column=3, padx=5, pady=5)

        # Pole "Wanted Fields"
        ttk.Label(colonize_frame, text="Wanted Fields:").grid(row=0, column=4, padx=5, pady=5)
        self.wanted_fields_entry = ttk.Entry(colonize_frame)
        self.wanted_fields_entry.grid(row=0, column=5, padx=5, pady=5)

        # Pole "Missions Num"
        ttk.Label(colonize_frame, text="Missions Num:").grid(row=0, column=6, padx=5, pady=5)
        self.mission_num_entry = ttk.Entry(colonize_frame)
        self.mission_num_entry.grid(row=0, column=7, padx=5, pady=5)

        # Przycisk "Colonize"
        self.colonize_button = ttk.Button(colonize_frame, text="Colonize", command=self.colonize_command)
        self.colonize_button.grid(row=0, column=8, padx=5, pady=5)

        # ------------------------------------------
        # -------------- LOGS ----------------------
        # ------------------------------------------
        self.logs_notebook = ttk.Notebook(self.logs_tab)
        self.logs_notebook.pack(fill="both", expand=True)

        log_tabs = {
            "Asteroid": "asteroid_log",
            "Expedition": "expedition_log",
            "General": "general_log",
            "Colonize": "colonize_log",
            "Plunder": "plunder_log"
        }

        for tab_name, attr_name in log_tabs.items():
            tab_frame = ttk.Frame(self.logs_notebook)
            self.logs_notebook.add(tab_frame, text=tab_name)

            log_frame = ttk.LabelFrame(tab_frame, text=f"{tab_name} Logs")
            log_frame.pack(fill="both", expand=True, padx=10, pady=5)

            # 🔍 Wyszukiwarka
            search_frame = ttk.Frame(log_frame)
            search_frame.pack(fill="x", padx=5, pady=2)

            search_var = tk.StringVar()

            entry = ttk.Entry(search_frame, textvariable=search_var)
            entry.pack(side="left", fill="x", expand=True)

            text_widget = tk.Text(log_frame, height=10, wrap="word")
            text_widget.pack(fill="both", expand=True, padx=5, pady=5)

            def make_search(widget, var):
                def search_logs(*_):
                    widget.tag_remove("highlight", "1.0", tk.END)
                    query = var.get()
                    if not query:
                        return
                    start = "1.0"
                    while True:
                        pos = widget.search(query, start, stopindex=tk.END)
                        if not pos:
                            break
                        end_pos = f"{pos}+{len(query)}c"
                        widget.tag_add("highlight", pos, end_pos)
                        widget.tag_config("highlight", background="yellow")
                        start = end_pos
                    if widget.tag_ranges("highlight"):
                        widget.see(widget.tag_ranges("highlight")[0])
                return search_logs

            search_var.trace_add("write", make_search(text_widget, search_var))

            setattr(self, attr_name, text_widget)

        
        # Przykładowa zawartość zakładki Settings
        build_asteroid_config_frame(self.settings_tab)
        build_expedition_config_frame(self.settings_tab)
        self.settings_tab.columnconfigure(0, weight=1)
        self.settings_tab.columnconfigure(1, weight=1)

        widget_handler = logger.WidgetHandler(self.asteroid_log, self.expedition_log, self.plunder_log, self.colonize_log, self.general_log )
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


    def toggle_plunder(self):
        if self.plunder_checkbox_var.get():
            threads.running_threads['plunder'].set()
            config.crons.plunder.enabled = True
            save_config()
        else:
            threads.running_threads['plunder'].clear()
            config.crons.plunder.enabled = False
            save_config()


    def colonize_command(self):
        coords_from = self.coords_from_entry.get()
        coords_to = self.coords_to_entry.get()
        wanted_fields = int(self.wanted_fields_entry.get())
        mission_num = int(self.mission_num_entry.get())
        
        base_planet = models.models.search_for_planet(models.models.planets, coords_from)
        t = threading.Thread(target=colonize_planet.colonize_planet, args= (base_planet, coords_to, wanted_fields, mission_num))
        t.start()
    

    def load_missions(self):
        """Ładuje misje do pamięci i ustawia początkowe wartości"""
        missions = fleet_service.get_missions()
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

        self.autoexpedition_list.insert("", "end", values=("Sum", "-", len(self.mission_data["Expedition"])))

        self.after(1000, self.refresh_view)  # Odśwież co sekundę


def build_asteroid_config_frame(parent):
    asteroid = config.crons.asteroid
    frame = ttk.LabelFrame(parent, text="Asteroid Config")
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    #frame.pack(fill="x", padx=10, pady=10)

    # enabled (checkbox)
    enabled_var = tk.BooleanVar(value=asteroid.enabled)
    ttk.Checkbutton(
        frame, text="Enabled", variable=enabled_var,
        command=lambda: [change_asteroid_is_enabled(enabled_var), save_config()]
    ).pack(anchor="w")

    def change_asteroid_is_enabled(enabled_var):
        asteroid.enabled = enabled_var.get()

    # is_from_moon (checkbox)
    moon_var = tk.BooleanVar(value=asteroid.is_from_moon)
    ttk.Checkbutton(
        frame, text="Is from Moon", variable=moon_var,
        command=lambda: [change_asteroid_is_from_moon(moon_var), save_config()]
    ).pack(anchor="w")

    def change_asteroid_is_from_moon(moon_var):
        asteroid.is_from_moon = moon_var.get()

    # miners_percentage
    percentage_var = tk.StringVar(value=str(asteroid.miners_percentage))

    def on_percentage_change(*_):
        try:
            config.crons.asteroid.miners_percentage = int(percentage_var.get())
            save_config()
        except ValueError:
            pass

    ttk.Label(frame, text="Miners %:").pack(anchor="w")
    ttk.Entry(frame, textvariable=percentage_var, width=5).pack(anchor="w")
    percentage_var.trace_add("write", on_percentage_change)

    # --- Asteroid Coords ---
    ttk.Label(frame, text="Asteroid Coords:").pack(anchor="w")

    coords_listbox = tk.Listbox(frame, height=15, width=30)
    coords_listbox.pack(pady=(0, 5), anchor="w")

    for coord in asteroid.coords:
        planet = models.search_for_planet(models.planets, coord)
        coords_listbox.insert(tk.END, planet)

    def open_planet_selection_window():
        # Tworzymy nowe okno
        planet_window = tk.Toplevel(frame)
        planet_window.title("Select Planet")
        
        # Lista planet
        planet_listbox = tk.Listbox(planet_window, height=10, width=30)
        planet_listbox.pack(padx=10, pady=10)

        # Zakładamy, że planet.planet zawiera listę dostępnych planet
        for planet in models.planets:
            planet_listbox.insert(tk.END, planet)

        def add_selected_planet():
            selected_planet = planet_listbox.curselection()
            if selected_planet:
                selected_planet = planet_listbox.get(selected_planet[0])
                coords = selected_planet.split(' ')[1]
                if coords not in asteroid.coords:
                    asteroid.coords.append(coords)
                    coords_listbox.insert(tk.END, coords)
                    save_config()
            planet_window.destroy()

        # Przyciski
        ttk.Button(planet_window, text="Add", command=add_selected_planet).pack(pady=5)
        ttk.Button(planet_window, text="Cancel", command=planet_window.destroy).pack(pady=5)

    # Przycisk do otwarcia okna wyboru planety
    ttk.Button(frame, text="Dodaj Planetę", command=open_planet_selection_window).pack(side="left", padx=5)

    def remove_selected_coord():
        selected = coords_listbox.curselection()
        if selected:
            index = selected[0]
            value = coords_listbox.get(index)
            asteroid.coords.remove(value.split(' ')[1])
            coords_listbox.delete(index)
            save_config()

    ttk.Button(frame, text="Usuń", command=remove_selected_coord).pack(side="left", padx=5)

    return frame

def build_expedition_config_frame(parent):
    expedition = config.crons.expedition
    frame = ttk.LabelFrame(parent, text="Expedition Config")
    frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    #frame.pack(fill="x", padx=10, pady=10)

    # enabled (checkbox)
    enabled_var = tk.BooleanVar(value=expedition.enabled)
    ttk.Checkbutton(
        frame, text="Enabled", variable=enabled_var,
        command=lambda: [set_enabled(), save_config()]
    ).pack(anchor="w")

    def set_enabled():
        expedition.enabled = enabled_var.get()

    # time (entry)
    time_var = tk.StringVar(value=str(expedition.time))

    def on_time_change(*_):
        try:
            expedition.time = int(time_var.get())
            save_config()
        except ValueError:
            pass

    ttk.Label(frame, text="Expedition Time (min):").pack(anchor="w")
    ttk.Entry(frame, textvariable=time_var, width=5).pack(anchor="w")
    time_var.trace_add("write", on_time_change)

    # send resources (checkbox)
    send_resources_var = tk.BooleanVar(value=expedition.send_resources)
    ttk.Checkbutton(
        frame, text="Send Resources", variable=send_resources_var,
        command=lambda: [set_send_resources(), save_config()]
    ).pack(anchor="w")

    def set_send_resources():
        expedition.send_resources = send_resources_var.get()

    # wanted deuterium (entry)
    wanted_deuterium_var = tk.StringVar(value=str(expedition.wanted_deuterium))

    def on_wanted_deuterium_change(*_):
        try:
            expedition.wanted_deuterium = int(wanted_deuterium_var.get())
            save_config()
        except ValueError:
            pass

    ttk.Label(frame, text="Wanted deuterium:").pack(anchor="w")
    ttk.Entry(frame, textvariable=wanted_deuterium_var, width=15).pack(anchor="w")
    wanted_deuterium_var.trace_add("write", on_wanted_deuterium_change)

    # --- Expedition Planets ---
    ttk.Label(frame, text="Expedition Planets:").pack(anchor="w")

    planets_listbox = tk.Listbox(frame, height=15, width=30)
    planets_listbox.pack(pady=(0, 5), anchor="w")

    for coord in expedition.planets:
        planet = models.search_for_planet(models.planets, coord)
        planets_listbox.insert(tk.END, planet)

    def open_planet_selection_window():
        planet_window = tk.Toplevel(frame)
        planet_window.title("Select Planet")

        planet_listbox = tk.Listbox(planet_window, height=10, width=30)
        planet_listbox.pack(padx=10, pady=10)

        for planet in models.planets:
            planet_listbox.insert(tk.END, planet)

        def add_selected_planet():
            selected = planet_listbox.curselection()
            if selected:
                selected_planet = planet_listbox.get(selected[0])
                coords = selected_planet.split(' ')[1]  # Zakładamy np. "Earth [6:123:7]"
                if coords not in expedition.planets:
                    expedition.planets.append(coords)
                    planets_listbox.insert(tk.END, selected_planet)
                    save_config()
            planet_window.destroy()

        ttk.Button(planet_window, text="Add", command=add_selected_planet).pack(pady=5)
        ttk.Button(planet_window, text="Cancel", command=planet_window.destroy).pack(pady=5)

    ttk.Button(frame, text="Dodaj Planetę", command=open_planet_selection_window).pack(side="left", padx=5)

    def remove_selected_planet():
        selected = planets_listbox.curselection()
        if selected:
            index = selected[0]
            display_value = planets_listbox.get(index)
            coords = display_value.split(' ')[1]
            expedition.planets.remove(coords)
            planets_listbox.delete(index)
            save_config()

    ttk.Button(frame, text="Usuń", command=remove_selected_planet).pack(side="left", padx=5)

    return frame



if __name__ == "__main__":
    app = App()

    threading.Thread(target=main_loop.run_crons, daemon=True).start()
    app.mainloop()
