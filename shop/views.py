from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from user.models import Profile
from .models import Product, Cart, Order, Size
from user.models import Address
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import uuid


def products(request):
    product = Product.objects.all()
    size = Size.objects.all()
    context = {
        'product': product,
        'size': size
    }
    return render(request, 'user/product.html', context)


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
    return render(request, 'user/shoping-cart.html', context)


@csrf_exempt
@login_required
def add_to_cart(request, p_id):
    user = request.user
    picked_size = request.POST['size']
    size = Size.objects.get(pk=picked_size)
    if Cart.objects.filter(user=user, product_id=p_id, size=size).exists():
        cart = Cart.objects.get(user=user, product_id=p_id, size=size)
        cart.quantity += 1
        cart.save()
    else:
        Cart.objects.create(user=user, product_id=p_id, size=size)
    return JsonResponse('true', safe=False)


@csrf_exempt
def remove_from_cart(request, id):
    product = Cart.objects.get(id=id)
    product.delete()
    return JsonResponse('true', safe=False)


@csrf_exempt
def add_quantity(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    carts = Cart.objects.filter(user=request.user)
    if cart.quantity > 19:
        return JsonResponse('false', safe=False)
    else:
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
    print(cart.quantity)
    if cart.quantity < 2:
        cart.delete()
    else:
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
        'total': total,
        # 'carts': serializers.serialize('json', carts)
    }
    return JsonResponse(data)


def product_view(request, id):
    product = Product.objects.get(id=id)
    size = Size.objects.all()
    context = {
        'product': product,
        'size': size
    }
    return render(request, 'user/product-detail.html', context)


def product_quick_view(request, id):
    product = Product.objects.filter(id=id)
    data = {
        'product1': serializers.serialize('json', product)
    }
    return JsonResponse(data)


@csrf_exempt
def place_order(request):
    user = request.user
    address = request.POST['address']
    if request.POST['data'] == 'True':
        status = True
    else:
        status = False
    carts = Cart.objects.filter(user=user)
    transaction_id = uuid.uuid4()
    address_id = Address.objects.get(id=address)
    for cart in carts:
        amount_paid = cart.product.price * cart.quantity
        Order.objects.create(user=user, product=cart.product, quantity=cart.quantity,
                             size=cart.size, payment_status=status, amount_paid=amount_paid, address=address_id,
                             transaction_id=transaction_id)
        amount_paid = 0
    carts.delete()
    return JsonResponse('true', safe=False)


@csrf_exempt
def payment_page(request):
    user = request.user
    address = Address.objects.filter(user=user)
    cart = Cart.objects.filter(user=user)
    total = 0
    for cart in cart:
        total = total + cart.product.price * cart.quantity
    paypal_total = "%.2f" % (total / 70)
    razorpay_total = int(total * 100)
    context = {
        'address': address,
        'total': total,
        'paypal_total': paypal_total,
        'razorpay_total': razorpay_total
    }
    return render(request, 'user/payment-page.html', context)


def order_confirm(request):
    return render(request, 'user/order-confirmed.html')


@csrf_exempt
def cancel_order(request,id):
    order = Order.objects.get(id=id)
    order.order_status = 'cancelled'
    order.save()
    return redirect('my-orders')


def confirm_order(request, id):
    order = Order.objects.get(id = id)
    order.order_status = 'confirmed'
    order.save()
    return redirect('orders')


def deliver_order(request, id):
    order = Order.objects.get(id = id)
    order.order_status = 'delivered'
    order.payment_status = True
    order.save()
    return redirect('orders')


def cancel_order_admin(request,id):
    order = Order.objects.get(id=id)
    order.order_status = 'cancelled'
    order.save()
    return redirect('orders')