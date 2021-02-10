from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.views.decorators.http import require_POST
# from .models import Product
# from .cart import Cart
# from .forms import CartAddProductForm


@login_required
def cart(request):
    return render(request, 'user/cart.html')
















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