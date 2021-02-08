from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='admin-home'),
    path('users/', views.user_view, name='user-view'),
    path('products/', views.product_view, name='product-view'),
    path('', views.admin_login, name='admin-login'),
    path('logout/', views.admin_logout, name='admin-logout'),
    path('add-product/', views.add_product, name='add-product'),
    path('delete/<int:id>', views.delete_user, name='delete-user'),
    path('delete-product/<int:id>', views.delete_product, name='delete-product'),
    path('edit-user/<int:id>', views.edit_user, name='edit-user'),
    path('edit-product/<int:id>', views.edit_product, name='edit-product')
]
