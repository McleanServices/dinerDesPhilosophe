from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/philosophers/', consumers.PhilosopherConsumer.as_asgi()),
]
