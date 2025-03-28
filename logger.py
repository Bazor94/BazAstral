import tkinter as tk
from tkinter import ttk
import logging
from models import planet

class TerminalHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        record.planet = getattr(record, "planet", "None")
        record.action = getattr(record, "action", "None")
        log_entry = self.format(record)
        print(log_entry)


class FileHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.files = {
            'asteroid': None,
            'expedition': None,
            'none': None
        }
        self._ensure_log_directory()

    def _ensure_log_directory(self):
        """Tworzy katalog logów, jeśli nie istnieje."""
        import os
        os.makedirs('logs', exist_ok=True)

    def _get_file(self, action):
        """Lazy initialization - otwiera plik tylko przy pierwszym użyciu."""
        if self.files[action] is None:
            try:
                self.files[action] = open(f'logs/{action}.log', 'a', encoding='utf-8')
            except Exception as e:
                print(f"Błąd otwarcia pliku {action}.log: {e}")
                return None
        return self.files[action]
    
    def emit(self, record):
        try:
            record.planet = getattr(record, "planet", "None")
            record.action = getattr(record, "action", "none")
            log_entry = self.format(record) + '\n'
            
            file = self._get_file(record.action) or self._get_file('none')
            if file:
                file.write(log_entry)
                file.flush()
        except Exception as e:
            print(f"Błąd zapisu logu: {e}")
    
    def close(self):
        """Bezpieczne zamykanie wszystkich plików."""
        for action, file in self.files.items():
            if file is not None:
                try:
                    file.close()
                except Exception as e:
                    print(f"Błąd przy zamykaniu pliku {action}.log: {e}")
        super().close()

class WidgetHandler(logging.Handler):
    def __init__(self, asteroid_widget, expedition_widget, rest_widget):
        super().__init__()
        self.asteroid_widget = asteroid_widget
        self.expedition_widget = expedition_widget
        self.rest_widget = rest_widget

    def emit(self, record):
        record.planet = getattr(record, "planet", "none")
        record.action = getattr(record, "action", "none")
        log_entry = self.format(record)

        if record.action == "asteroid":
            widget = self.asteroid_widget
        elif record.action == "expedition":
            widget = self.expedition_widget
        elif record.action == "none":
            widget = self.rest_widget

        widget.insert("end", log_entry + "\n")
        widget.see("end") 


logger = logging.getLogger(__name__)
terminal_handler = TerminalHandler()
terminal_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(action)s | %(planet)s | %(message)s'))
logger.addHandler(terminal_handler)

file_handler = FileHandler()
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(planet)s | %(message)s'))
logger.addHandler(file_handler)

logger.setLevel(logging.INFO)
