from django.urls import path
from . import views
from shop import views as shop_view


urlpatterns = [
    path('', views.index, name = 'index'),
    path('signup/', views.register, name = 'signup'),
    path('login/', views.login_user, name = 'signin'),
    path('logout/', views.logout_user, name = 'logout'),
    path('cart/', shop_view.cart, name = 'cart'),
    path('add_cart/<int:p_id>', shop_view.add_to_cart, name='add-cart'),
    path('add_quantity/<int:cart_id>', shop_view.add_quantity, name='add-quantity')
]