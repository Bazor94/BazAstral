import tkinter as tk
from tkinter import ttk
import logging
import models

class TerminalHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        record.planet = getattr(record, "planet", "None")
        record.action = getattr(record, "action", "None")
        log_entry = self.format(record)
        print(log_entry)

class WidgetHandler(logging.Handler):
    def __init__(self, asteroid_widget, expedition_widget, general_widget):
        super().__init__()
        self.asteroid_widget = asteroid_widget
        self.expedition_widget = expedition_widget
        self.general_widget = general_widget

    def emit(self, record):
        record.planet = getattr(record, "planet", "none")
        record.action = getattr(record, "action", "none")
        log_entry = self.format(record)

        if record.action == "asteroid":
            widget = self.asteroid_widget
        elif record.action == "expedition":
            widget = self.expedition_widget
        else:
            widget = self.general_widget

        widget.insert("end", log_entry + "\n")
        widget.see("end") 


logger = logging.getLogger(__name__)
terminal_handler = TerminalHandler()
terminal_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(action)s | %(planet)s | %(message)s'))
logger.addHandler(terminal_handler)
logger.setLevel(logging.INFO)
