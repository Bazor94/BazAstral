import tkinter as tk
from tkinter import ttk
import logging
import models
from datetime import datetime, timedelta

class TerminalHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        record.planet = getattr(record, "planet", "None")
        record.action = getattr(record, "action", "None")
        log_entry = self.format(record)
        print(log_entry)

class WidgetHandler(logging.Handler):
    def __init__(self, asteroid_widget, expedition_widget, plunder_widget, colonize_widget, general_widget):
        super().__init__()
        self.asteroid_widget = asteroid_widget
        self.expedition_widget = expedition_widget
        self.plunder_widget = plunder_widget
        self.colonize_widget = colonize_widget
        self.general_widget = general_widget

    def emit(self, record):
        record.planet = getattr(record, "planet", "none")
        record.action = getattr(record, "action", "none")
        log_entry = self.format(record)

        if record.action == "asteroid":
            widget = self.asteroid_widget
        elif record.action == "expedition":
            widget = self.expedition_widget
        elif record.action == "plunder":
            widget = self.plunder_widget
        elif record.action == "colonize":
            widget = self.colonize_widget
        else:
            widget = self.general_widget

        widget.insert("end", log_entry + "\n")


def sleep_log(action, planet, time_sleep, prefix=""):
    formatted_time = (datetime.now() + timedelta(seconds=time_sleep)).strftime("%H:%M:%S")
    log_string = f'sleeping for {format_seconds(time_sleep)}. Till {formatted_time}'
    if prefix != "":
        log_string = prefix + " " + log_string

    logger.info(log_string, extra={"planet": planet, "action": action})


logger = logging.getLogger(__name__)
terminal_handler = TerminalHandler()
terminal_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(action)s | %(planet)s | %(message)s'))
logger.addHandler(terminal_handler)
logger.setLevel(logging.DEBUG)
setattr(logger, "sleep_log", sleep_log)


def format_seconds(time_needed):
    minutes = time_needed // 60  # Dzielenie całkowite, aby uzyskać minuty
    seconds = time_needed % 60  # Reszta z dzielenia, aby uzyskać sekundy
    return f"{minutes:02}:{seconds:02}"  # Formatuje w postaci mm:ss
