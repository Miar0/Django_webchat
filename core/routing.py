from django.urls import path

from core import consumers

ws_routes = {
    path('ws/chat', consumers.ChatConsumer.as_asgi())
}
