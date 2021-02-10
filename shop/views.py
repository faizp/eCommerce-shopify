from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.views.decorators.http import require_POST
from .models import Product, Cart
# from .forms import CartAddProductForm



def cart(request):
    return render(request, 'user/cart.html')

@login_required
def add_to_cart(request,p_id):
    user = request.user.id
    print(user)
    product = Product.objects.get(id=p_id)
    us = User.objects.get(pk=user)
    cart = Cart.objects.create(user_id = us, product_id = product)
    cart.save()
    print(cart)
    return redirect('cart')
















# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,quantity=cd['quantity'], ovverride_quantity=cd['ovveride'])
#     return redirect('cart:cart_detail')
#
# @require_POST
# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return redirect('cart:cart_detail')