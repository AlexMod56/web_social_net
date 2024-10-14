from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('users/', views.user_list_view, name='user-list'),
    path('users/profile/<str:username>/', views.profile_read_only_view, name='profile-read-only'),

]
