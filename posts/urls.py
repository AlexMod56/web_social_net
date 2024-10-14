from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
    path('post/create/', views.post_create, name='post-create'),
]
