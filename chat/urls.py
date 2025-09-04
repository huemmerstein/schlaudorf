"""URL routes for chat-related views."""
from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('dm/', views.direct, name='direct'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('user/<str:username>/', views.profile_detail, name='profile_detail'),
]
