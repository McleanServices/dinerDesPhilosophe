from django.shortcuts import render
from django.http import JsonResponse
from .models import Philosopher
from .simulation import start_simulation, stop_simulation
import threading

def index(request):
    return render(request, 'polls/index.html')  # Render the index.html template

def philosopher_states(request):
    philosophers = Philosopher.objects.all().values("name", "state", "updated_at")
    return JsonResponse(list(philosophers), safe=False)

def reset_philosophers(request):
    Philosopher.reset_states()
    return JsonResponse({"status": "Philosophers' states reset successfully."})

def start_dinner(request):
    thread = threading.Thread(target=start_simulation)
    thread.start()
    return render(request, 'polls/simulation_started.html')  # Render a template with a button

def stop_simulation_view(request):
    if request.method == "POST":
        stop_simulation()
        return JsonResponse({"message": "Simulation stopped successfully."})
    return JsonResponse({"error": "Invalid request method."}, status=405)
