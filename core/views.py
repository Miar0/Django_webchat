from django.shortcuts import render, get_object_or_404
from django.views.generic import *

from core.models import Room, Message


class ChatView(TemplateView):
    template_name = 'chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = get_object_or_404(Room, id=self.kwargs.get('room_id'))
        context['messages'] = Message.objects.filter(room_id=self.kwargs.get('room_id'))
        return context


class RoomListView(ListView):
    template_name = 'rooms.html'
    model = Room
    context_object_name = 'rooms'
