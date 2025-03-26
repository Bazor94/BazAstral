import threading
import queue
import time

# Tworzymy kolejkę z maksymalnym rozmiarem 5
q = queue.Queue(maxsize=5)

def producer():
    pass

def consumer():
    try:
        item = q.get_nowait()  # Pobranie produktu z kolejki
    except queue.Empty:
        print("empty")

    print(f"Konsument: Pobieram {item}")
        

# Uruchamiamy wątki
t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer, daemon=True)  # Konsument działa w nieskończonej pętli

t1.start()
t2.start()

# Czekamy na zakończenie produkcji
t1.join()

# Upewniamy się, że wszystkie zadania zostały przetworzone
q.join()

print("Wszystkie produkty zostały przetworzone!")
