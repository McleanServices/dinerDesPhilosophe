import threading
import time
import random
import logging
from .models import Philosopher

# Create a lock for each fork
forks = []
threads = []
stop_event = threading.Event()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def philosopher_simulation(philosopher_id, left_fork, right_fork, reverse_order=False):
    while not stop_event.is_set():
        philosopher = Philosopher.objects.get(id=philosopher_id)
        philosopher.state = "Réfléchit 🤔"
        philosopher.save()
        logging.info(f"Philosopher {philosopher_id} is thinking.")
        time.sleep(random.randint(2, 5))

        # Alternate fork-picking order for deadlock prevention
        first_fork, second_fork = (right_fork, left_fork) if reverse_order else (left_fork, right_fork)

        # Try to pick up the first fork
        with first_fork:
            philosopher.state = "Prend la fourchette gauche 🥄" if not reverse_order else "Prend la fourchette droite 🥄"
            philosopher.save()
            logging.info(f"Philosopher {philosopher_id} picked up the first fork.")
            time.sleep(random.randint(1, 3))

            # Try to pick up the second fork
            with second_fork:
                philosopher.state = "Prend la fourchette droite 🥄" if not reverse_order else "Prend la fourchette gauche 🥄"
                philosopher.save()
                logging.info(f"Philosopher {philosopher_id} picked up the second fork.")
                time.sleep(random.randint(1, 3))

                # Eating
                philosopher.state = "Mange 🍽️"
                philosopher.save()
                logging.info(f"Philosopher {philosopher_id} is eating.")
                time.sleep(random.randint(2, 5))

        # Release forks automatically when exiting the `with` blocks

def start_simulation():
    global forks, threads
    philosophers = Philosopher.objects.all()
    num_philosophers = philosophers.count()

    # Initialize a lock for each fork
    forks = [threading.Lock() for _ in range(num_philosophers)]

    for i, philosopher in enumerate(philosophers):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % num_philosophers]  # Circular arrangement of forks
        reverse_order = (i == num_philosophers - 1)  # Last philosopher picks forks in reverse order
        thread = threading.Thread(target=philosopher_simulation, args=(philosopher.id, left_fork, right_fork, reverse_order))
        threads.append(thread)
        thread.start()

def stop_simulation():
    global threads
    stop_event.set()  # Signal all threads to stop
    for thread in threads:
        thread.join()  # Wait for all threads to finish
    logging.info("Simulation stopped.")
