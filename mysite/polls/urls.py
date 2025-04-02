from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_dinner, name='start_dinner'),  # Root URL starts the simulation
    path('start/', views.index, name='index'),  # Navigate to the simulation page
    path('reset/', views.reset_philosophers, name='reset_philosophers'),
    path('philosopher_states/', views.philosopher_states, name='philosopher_states'),
    path('stop/', views.stop_simulation_view, name='stop_simulation'),
]
