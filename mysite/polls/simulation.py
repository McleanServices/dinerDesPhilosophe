import threading
import time
import random
import logging
from .models import Philosopher

# Création d'un verrou pour chaque fourchette
forks = []
threads = []
stop_event = threading.Event()

# Configuration du système de journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def philosopher_simulation(philosopher_id, left_fork, right_fork, reverse_order=False):
    while not stop_event.is_set():
        philosopher = Philosopher.objects.get(id=philosopher_id)
        philosopher.state = "Réfléchit 🤔"
        philosopher.save()
        logging.info(f"Philosophe {philosopher_id} est en train de réfléchir.")
        time.sleep(random.randint(2, 5))

        # Alternance de l'ordre de prise des fourchettes pour éviter les interblocages
        first_fork, second_fork = (right_fork, left_fork) if reverse_order else (left_fork, right_fork)

        # Tentative de prendre la première fourchette
        with first_fork:
            philosopher.state = "Prend la fourchette gauche 🥄" if not reverse_order else "Prend la fourchette droite 🥄"
            philosopher.save()
            logging.info(f"Philosophe {philosopher_id} a pris la première fourchette.")
            time.sleep(random.randint(1, 3))

            # Tentative de prendre la deuxième fourchette
            with second_fork:
                philosopher.state = "Prend la fourchette droite 🥄" if not reverse_order else "Prend la fourchette gauche 🥄"
                philosopher.save()
                logging.info(f"Philosophe {philosopher_id} a pris la deuxième fourchette.")
                time.sleep(random.randint(1, 3))

                # Phase de repas
                philosopher.state = "Mange 🍽️"
                philosopher.save()
                logging.info(f"Philosophe {philosopher_id} est en train de manger.")
                time.sleep(random.randint(2, 5))

        # Les fourchettes sont automatiquement libérées à la sortie des blocs `with`

def start_simulation():
    global forks, threads
    philosophers = Philosopher.objects.all()
    num_philosophers = philosophers.count()

    # Initialisation d'un verrou pour chaque fourchette
    forks = [threading.Lock() for _ in range(num_philosophers)]

    for i, philosopher in enumerate(philosophers):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % num_philosophers]  # Arrangement circulaire des fourchettes
        reverse_order = (i == num_philosophers - 1)  # Le dernier philosophe prend les fourchettes dans l'ordre inverse
        thread = threading.Thread(target=philosopher_simulation, args=(philosopher.id, left_fork, right_fork, reverse_order))
        threads.append(thread)
        thread.start()

def stop_simulation():
    global threads
    stop_event.set()  # Signal pour arrêter tous les threads
    for thread in threads:
        thread.join()  # Attente de la fin de tous les threads
    logging.info("La simulation a été arrêtée.")
