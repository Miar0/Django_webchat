"""
URL configuration for django_webchat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from core.views import *
from django_webchat import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('chat/<int:room_id>', ChatView.as_view()),
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view(template_name='login.html')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('rooms/<int:room_id>', ChatDataView.as_view(), name='chat_data'),
    path('rooms/', RoomListView.as_view(), name='rooms'),
    path('sent-friend-request/', SendRequestsView.as_view(), name='sent_friend_request'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('friends/', ListFriendView.as_view(), name='friends'),
    path('friend-requests/', FriendRequestView.as_view(), name='friend_requests'),
    path('cancel-friend-request/<int:pk>', CancelRequestView.as_view(), name='cancel_friend_request'),
    path('remove-friend/<int:pk>', RemoveFriendView.as_view(), name='remove_friend'),
    path('accept-friend-request/<int:pk>', AcceptFriendView.as_view(), name='accept_friend_request'),
    path('reject-friend-request/<int:pk>', RejectFriendView.as_view(), name='reject_friend_request')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)