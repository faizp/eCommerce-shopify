from django.urls import path
from . import views
from shop import views as shop_view

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', shop_view.products, name='products'),
    path('signup/', views.register, name='signup'),
    path('login/', views.login_user, name='signin'),
    path('logout/', views.logout_user, name='logout'),
    path('cart/', shop_view.cart, name='cart'),
    path('add_cart/<int:p_id>', shop_view.add_to_cart, name='add-cart'),
    path('add_quantity/<int:cart_id>', shop_view.add_quantity, name='add-quantity'),
    path('reduce_quantity/<int:cart_id>', shop_view.reduce_quantity, name='reduce-quantity'),
    path('remove_from_cart/<int:id>', shop_view.remove_from_cart, name='remove-from-cart'),
    path('product/<int:id>', shop_view.product_view, name='product-view'),
    path('profile/', views.profile, name='user-profile'),
    path('address/', views.addresses, name='user-addresses'),
    path('add_new_address/', views.add_new_address, name='add-new-address'),
    path('delete_address/<int:id>', views.delete_address, name='delete-address'),
    path('edit-address/<int:id>', views.edit_address, name='edit-address'),
    path('otp-login/', views.phone, name='otp-login'),
    path('otp/', views.otp_login, name='otp-verify'),
    path('place-order/', shop_view.place_order, name='place-order'),
    path('payment-page/', shop_view.payment_page, name='payment-page'),
    path('register/', views.register_user, name = 'register-user'),
    path('order-confirm/', shop_view.order_confirm, name='order-confirm'),
    path('my-orders/', views.my_orders, name='my-orders'),
    path('cancel-order/<int:id>', shop_view.cancel_order, name='cancel-order'),
    path('quick-view/<int:id>', shop_view.product_quick_view, name='product-quick-view'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
