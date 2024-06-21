from django.urls import path

from core import consumers

ws_routes = {
    path('ws/chat/<int:room_id>', consumers.ChatConsumer.as_asgi())
}
