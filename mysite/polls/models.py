from django.db import models

# Create your models here.

class Philosopher(models.Model):
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=20, default="Thinking")  # e.g., Thinking, Eating, Taking Fork
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}: {self.state}"

    @staticmethod
    def reset_states():
        states = {
            "Socrates": "Eating",
            "Plato": "Hungry",
            "Aristotle": "Hungry",
            "Descartes": "Thinking",
            "Kant": "Hungry"
        }
        for name, state in states.items():
            Philosopher.objects.update_or_create(name=name, defaults={"state": state})
