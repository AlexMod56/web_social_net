from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat-home'),
    path('<int:pk>/', views.chat_detail, name='chat-detail'),
    path('create/', views.chat_create, name='chat-create'),
]
