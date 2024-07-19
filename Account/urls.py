from django.contrib import admin
from django.urls import path
from .views import Register,generate, error,Login,CreateRoom, Chat, JoinRoom, indes, createse, message

urlpatterns = [
    path('', indes, name="index"),
    path('create_pase', createse, name="created"),
    path('message/<str:chatcode>/', message, name="message"),
    path('register', Register.as_view(), name='register'),
    path('create', CreateRoom.as_view(), name='create'),
    path('join_room', JoinRoom.as_view(), name='join'),
    path('chat/<str:chatcode>/', Chat.as_view(), name='chat'),  # Dynamic URL with chatcode
    path('login', Login.as_view(), name='login'),
    path('generate',generate, name='generate'),
    path('error',error, name='error'), 
]
