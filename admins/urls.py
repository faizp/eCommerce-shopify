from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name = 'admin-home'),
    path('users/', views.user_view, name = 'user-view'),
    path('', views.admin_login, name = 'admin-login'),
    path('logout/', views.admin_logout, name = 'admin-logout')
]