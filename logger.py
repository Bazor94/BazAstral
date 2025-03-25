import tkinter as tk
from tkinter import ttk
import logging

class WidgetHandler(logging.Handler):
    def __init__(self, asteroid_widget, expedition_widget, rest_widget):
        super().__init__()
        self.asteroid_widget = asteroid_widget
        self.expedition_widget = expedition_widget
        self.rest_widget = rest_widget

    def emit(self, record):
        record.planet = getattr(record, "planet", "None")
        record.action = getattr(record, "action", "None")
        log_entry = self.format(record)
        print(log_entry)

        
        # self.text_widget.insert("end", log_entry + "\n")
        # self.text_widget.see("end")  # Automatyczne przewijanie na dół


logger = logging.getLogger(__name__)
handler = WidgetHandler(None, None, None)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(action)s | %(planet)s | %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.info('xd', extra={"planet": "Aden [3:12:5]", "action": "expedition"})



