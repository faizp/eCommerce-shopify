from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Product, Cart
from user.models import Address
from django.views.decorators.csrf import csrf_exempt


@login_required
def cart(request):
    user = request.user.id
    carts = Cart.objects.filter(user_id=user)
    total = 0
    for cart in carts:
        total = total + cart.product.price * cart.quantity
        cart.total = cart.product.price * cart.quantity
    context = {
        'carts': carts,
        'total': total
    }
    return render(request, 'user/cart.html', context)


@csrf_exempt
@login_required
def add_to_cart(request, p_id):
    user = request.user
    if Cart.objects.filter(user=user, product_id=p_id).exists():
        cart = Cart.objects.get(user=user, product_id=p_id)
        cart.quantity += 1
        cart.ordered = False
        cart.save()
    else:
        Cart.objects.create(user=user, product_id=p_id)
    return JsonResponse('true', safe=False)


def remove_from_cart(request, id):
    product = Cart.objects.get(id=id)
    product.delete()
    return redirect('cart')


@csrf_exempt
def add_quantity(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    carts = Cart.objects.filter(user=request.user)
    cart.quantity += 1
    cart.save()
    item_total = cart.quantity * cart.product.price
    total = 0
    for x in carts:
        total = total + x.quantity * x.product.price
    data = {
        'quantity': cart.quantity,
        'item_total': item_total,
        'total': total
    }
    return JsonResponse(data)


@csrf_exempt
def reduce_quantity(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.quantity -= 1
    cart.save()
    item_total = cart.quantity * cart.product.price
    carts = Cart.objects.filter(user_id=request.user)
    total = 0
    for x in carts:
        total = total + x.product.price * x.quantity
    data = {
        'quantity': cart.quantity,
        'item_total': item_total,
        'total': total
    }
    return JsonResponse(data)


def product_view(request, id):
    product = Product.objects.get(id=id)
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


def place_order(request):
    pass
#     user = request.user
#     # if request.method == 'POST':
#     # address = request.POST['address']
#     # print(address)
#     address = Address.objects.filter(user=user).first()
#     cart = Cart.objects.filter(user=user)
#     total = 0
#     for cart in cart:
#         total = total + cart.product.price * cart.quantity
#         cart.ordered = True
#         cart.save()
#     print(total)
#     Order.objects.create(user=user, address=address, amount=total)
#     return redirect('order-confirm')
#     # else:
#     #     return redirect('payment-page')


def payment_page(request):
    user = request.user
    address = Address.objects.filter(user=user)
    cart = Cart.objects.filter(user=user)
    total = 0
    for cart in cart:
        total = total + cart.product.price * cart.quantity

    context = {
        'address': address,
        'total': total
    }
    return render(request, 'user/payment-page.html', context)


def order_confirm(request):
    return render(request, 'user/order-confirmed.html')
