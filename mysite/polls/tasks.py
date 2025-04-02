import time
import random
from threading import Lock
from .models import Philosopher

# Global lock to act as the arbitrator
arbitrator_lock = Lock()

def update_philosophers():
    philosophers = list(Philosopher.objects.all())
    random.shuffle(philosophers)  # Randomize the order to avoid bias

    for philosopher in philosophers:
        with arbitrator_lock:  # Ensure only one philosopher can modify state at a time
            if philosopher.state == "Thinking":
                philosopher.state = "Hungry"
                philosopher.save()
            elif philosopher.state == "Hungry":
                eating_count = Philosopher.objects.filter(state="Eating").count()
                if eating_count < len(philosophers) - 1:  # Ensure at least one philosopher is not eating
                    philosopher.state = "Eating"
                    philosopher.save()
            elif philosopher.state == "Eating":
                philosopher.state = "Thinking"
                philosopher.save()