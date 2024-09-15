from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *

from core.forms import RegistrationForm
from core.models import *


# class ChatView(LoginRequiredMixin, TemplateView):
#     template_name = 'html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['room'] = get_object_or_404(Room, id=self.kwargs.get('room_id'))
#         context['messages'] = Message.objects.filter(room_id=self.kwargs.get('room_id'))
#         return context
#

class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ChatDataView(LoginRequiredMixin, View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        if request.user not in room.users.all():
            return JsonResponse(
                {
                    'error': 'You are not a member of this room'
                }, status=403
            )
        messages = Message.objects.filter(room=room)
        other_user = room.get_other_user(request.user)
        return render(request, 'chat_data.html', {
            'room': room,
            'messages': messages,
            'other_user': other_user
        })


class RoomListView(LoginRequiredMixin, ListView):
    template_name = 'rooms.html'
    model = Room
    context_object_name = 'rooms'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['rooms_with_users'] = [
            (room, room.get_other_user(user)) for room in self.get_queryset()
        ]
        return context

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(users=user)  # users_in = [user]


class SendRequestsView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        to_user_id = request.POST.get('to_user_id')
        to_user = get_object_or_404(SocialUser, id=to_user_id)
        from_user = request.user

        if not FriendRequests.objects.filter(from_user=from_user, to_user=to_user).exists():
            FriendRequests.objects.create(from_user=from_user, to_user=to_user)

        return redirect('user_list')


class AcceptFriendView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        friend_request_id = kwargs.get('pk')
        friend_request = get_object_or_404(FriendRequests, id=friend_request_id, to_user=request.user)

        if friend_request:
            friend_request.accept()
        return redirect('friend_requests')


class CancelRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        friend_request = get_object_or_404(FriendRequests, from_user=request.user, to_user=pk)
        friend_request.delete()
        return redirect('user_list')


class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        other_user = SocialUser.objects.get(id=pk)
        friend_request = get_object_or_404(
            FriendRequests, Q(from_user=request.user, to_user=pk) | Q(to_user=request.user, from_user=pk)
        )
        Room.objects.filter(
            Q(
                name=f"{request.user.username} -> {other_user.username}"
            ) | Q(
                name=f"{other_user.username} -> {request.user.username}")
        ).delete()

        friend_request.delete()
        return redirect('friends')


class RejectFriendView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        friend_request_id = kwargs.get('pk')
        friend_request = get_object_or_404(FriendRequests, id=friend_request_id, to_user=request.user)

        if friend_request:
            friend_request.delete()
        return redirect('friend_requests')


class FriendRequestView(LoginRequiredMixin, ListView):
    model = FriendRequests
    template_name = 'friend_requests.html'
    context_object_name = 'friend_requests'

    def get_queryset(self):
        return FriendRequests.objects.filter(to_user=self.request.user, accepted=False)


class ListFriendView(LoginRequiredMixin, ListView):
    model = SocialUser
    template_name = 'friend_list.html'
    context_object_name = 'friends'

    def get_queryset(self):
        friends = SocialUser.objects.filter(
            from_user__to_user=self.request.user, from_user__accepted=True
        ) | SocialUser.objects.filter(
            to_user__from_user=self.request.user, to_user__accepted=True
        )
        return friends


class UserListView(LoginRequiredMixin, ListView):
    model = SocialUser
    template_name = 'users.html'
    context_object_name = 'users'

    def get_queryset(self):
        current_user = self.request.user
        friends = SocialUser.objects.filter(
            from_user__to_user=self.request.user, from_user__accepted=True
        ) | SocialUser.objects.filter(
            to_user__from_user=self.request.user, to_user__accepted=True
        )

        received_requests = FriendRequests.objects.filter(to_user=current_user).values_list('from_user', flat=True)
        excluded_users = (
            set(received_requests)
            .union(set(friends.values_list('id', flat=True)))
            .union([current_user.id])
        )

        return SocialUser.objects.exclude(id__in=excluded_users)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        friend_request_sent = FriendRequests.objects.filter(from_user=current_user)
        context['friend_request_sent'] = [req.to_user.id for req in friend_request_sent]
        return context


