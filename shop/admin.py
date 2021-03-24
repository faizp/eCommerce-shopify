from django.contrib import admin
from .models import Product, Category, Cart, Size, Offer, Order, Coupon


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Size)
admin.site.register(Order)
admin.site.register(Offer)
admin.site.register(Coupon)
