from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.views.decorators.http import require_POST
from .models import Product, Cart
# from .forms import CartAddProductForm


@login_required
def cart(request):
    user = request.user.id
    carts = Cart.objects.filter(user_id=user)
    context = {
        'carts': carts,

    }
    return render(request, 'user/cart.html', context)

@login_required
def add_to_cart(request,p_id):
    Cart.objects.create(user = request.user, product_id = p_id)
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