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


@csrf_exempt
def add_quantity(request,cart_id):
    cart = Cart.objects.get(id = cart_id)
    cart.quantity += 1
    cart.save()
    context = {
        'quantity': cart.quantity,
        'price': cart.product.price
    }
    return JsonResponse(context)


@csrf_exempt
def reduce_quantity(request, cart_id):
    cart = Cart.objects.get(id = cart_id)
    cart.quantity -= 1
    cart.save()
    return JsonResponse({'quantity': cart.quantity})


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


def men(request):
    products = Product.objects.filter(sec_category='Male')
    print(products)
    context = {
        'products': products
    }
    return render(request, 'user/men.html', context)


def women(request):
    products = Product.objects.filter(sec_category='Female')
    print(products)
    context = {
        'products': products
    }
    return render(request, 'user/men.html', context)


def kids(request):
    products = Product.objects.filter(sec_category='Kids')
    print(products)
    context = {
        'products': products
    }
    return render(request, 'user/men.html', context)