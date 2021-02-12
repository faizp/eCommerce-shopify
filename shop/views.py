from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Product, Cart
from django.views.decorators.csrf import csrf_exempt


@login_required
def cart(request):
    user = request.user.id
    carts = Cart.objects.filter(user_id=user)
    context = {
        'carts': carts,

    }
    return render(request, 'user/cart.html', context)


@csrf_exempt
@login_required
def add_to_cart(request,p_id):
    user = request.user
    if Cart.objects.filter(user=user, product_id=p_id).exists():
        cart = Cart.objects.get(user=user, product_id=p_id)
        cart.quantity += 1
        cart.save()
    else:
        Cart.objects.create(user = user, product_id = p_id)
    return JsonResponse('true', safe=False)


def remove_from_cart(request, id):
    product = Cart.objects.get(id=id)
    product.delete()
    return redirect('cart')


def add_quantity(request,cart_id):
    pass


def product_view(request,id):
    product = Product.objects.get(id=id)
    print(product)
    print(product.image2)
    print(product.image3)
    print(product.image1)
    context = {
        'product': product
    }
    return render(request, 'user/product-view.html', context)










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