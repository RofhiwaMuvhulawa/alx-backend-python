from django.urls import path
from . import views

urlpatterns = [
    path('chatrooms/', views.ChatRoomList.as_view(), name='chatroom-list'),
    path('chatrooms/<int:pk>/', views.ChatRoomDetail.as_view(), name='chatroom-detail'),
]