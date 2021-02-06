from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = 'admin-home'),
    path('users/', views.user_view, name = 'user-view')
]