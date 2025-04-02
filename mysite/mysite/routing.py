from django.urls import path
from polls.consumers import PhilosopherConsumer

websocket_urlpatterns = [
    path('ws/philosophers/', PhilosopherConsumer.as_asgi()),
]
