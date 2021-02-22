from django.urls import path
from . import views
from shop import views as shop_view

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.register, name='signup'),
    path('login/', views.login_user, name='signin'),
    path('logout/', views.logout_user, name='logout'),
    path('cart/', shop_view.cart, name='cart'),
    path('add_cart/<int:p_id>', shop_view.add_to_cart, name='add-cart'),
    path('add_quantity/<int:cart_id>', shop_view.add_quantity, name='add-quantity'),
    path('reduce_quantity/<int:cart_id>', shop_view.reduce_quantity, name='reduce-quantity'),
    path('remove_from_cart/<int:id>', shop_view.remove_from_cart, name='remove-from-cart'),
    path('product/<int:id>', shop_view.product_view, name='product-view'),
    path('men/', shop_view.men, name='men-category'),
    path('women/', shop_view.women, name='women-category'),
    path('kids/', shop_view.kids, name='kids-category'),
]
