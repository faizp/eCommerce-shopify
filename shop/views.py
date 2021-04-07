from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, Cart, Order, Size, Offer
from user.models import Address, Profile
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import uuid
from datetime import date


def products(request):
    products = Product.objects.all()
    for product in products:
        offer = Offer.objects.filter(category=product.category, start_date__lte=date.today(),
                                     end_date__gte=date.today()).first()
        if offer is not None:
            product.offerPrice = product.price - (product.price * offer.discount) / 100
        else:
            product.offerPrice = product.price
    size = Size.objects.all()
    context = {
        'product': products,
        'size': size
    }
    return render(request, 'user/product.html', context)


@login_required(login_url='signin')
def cart(request):
    user = request.user.id
    carts = Cart.objects.filter(user_id=user)
    total = 0
    for cart in carts:
        offer = Offer.objects.filter(category=cart.product.category, start_date__lte=date.today(),
                                     end_date__gte=date.today()).first()
        if offer is not None:
            cart.product.offerPrice = cart.product.price - (cart.product.price * offer.discount) / 100
        else:
            cart.product.offerPrice = cart.product.price

        cart.total = cart.product.offerPrice * cart.quantity
        total = total + cart.product.offerPrice * cart.quantity

    request.session['total'] = total
    context = {
        'carts': carts,
        'total': total
    }
    return render(request, 'user/shoping-cart.html', context)


@csrf_exempt
@login_required(login_url='signin')
def add_to_cart(request, p_id):
    user = request.user
    picked_size = request.POST['size']
    size = Size.objects.get(pk=picked_size)
    cart_count = Cart.objects.filter(user=user).count()
    product = Product.objects.get(id=p_id)
    if Cart.objects.filter(user=user, product_id=p_id, size=size).exists():
        stock = Product.objects.get(id=p_id).stock
        cart = Cart.objects.get(user=user, product_id=p_id, size=size)
        if cart.quantity >= stock:
            return JsonResponse('false', safe=False)
        else:
            cart = Cart.objects.get(user=user, product_id=p_id, size=size)
            cart.quantity += 1
            cart.save()
    else:
        if Product.objects.get(id=p_id).stock < 1:
            return JsonResponse('false', safe=False)
        else:
            Cart.objects.create(user=user, product_id=p_id, size=size)
    data = {
        'count': cart_count,
        'name': product.name
    }
    return JsonResponse(data)


@csrf_exempt
def remove_from_cart(request, id):
    product = Cart.objects.get(id=id)
    product.delete()
    return redirect('cart')


@csrf_exempt
@login_required(login_url='signin')
def add_quantity(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    stock = Product.objects.get(id=cart.product_id).stock
    if cart.quantity >= stock:
        return JsonResponse('true', safe=False)
    else:
        cart.quantity += 1
        cart.save()
    total = 0
    offer = Offer.objects.filter(category=cart.product.category, start_date__lte=date.today(),
                                 end_date__gte=date.today()).first()
    if offer is not None:
        cart.product.offerPrice = cart.product.price - (cart.product.price * offer.discount) / 100
    else:
        cart.product.offerPrice = cart.product.price
    item_total = cart.product.offerPrice * cart.quantity
    total = total + cart.product.offerPrice * cart.quantity
    data = {
        'quantity': cart.quantity,
        'item_total': item_total,
        'total': total
    }
    return JsonResponse(data)


@csrf_exempt
@login_required(login_url='signin')
def reduce_quantity(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    print(cart.quantity)
    cart.quantity -= 1
    print('after ', cart.quantity)
    cart.save()
    if cart.quantity < 1:
        cart.delete()
        return JsonResponse('false', safe=False)
    total = 0
    offer = Offer.objects.filter(category=cart.product.category, start_date__lte=date.today(),
                                 end_date__gte=date.today()).first()
    if offer is not None:
        cart.product.offerPrice = cart.product.price - (cart.product.price * offer.discount) / 100
    else:
        cart.product.offerPrice = cart.product.price

    item_total = cart.product.offerPrice * cart.quantity
    total = total + cart.product.offerPrice * cart.quantity
    data = {
        'quantity': cart.quantity,
        'item_total': item_total,
        'total': total,
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
@login_required(login_url='signin')
def place_order(request):
    user = request.user
    del request.session['total']
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
        product = Product.objects.get(id=cart.product.id)
        product.stock = product.stock - cart.quantity
        product.save()
        Order.objects.create(user=user, product=cart.product, quantity=cart.quantity,
                             size=cart.size, payment_status=status, amount_paid=amount_paid, address=address_id,
                             transaction_id=transaction_id)
        amount_paid = 0
    carts.delete()
    return JsonResponse('true', safe=False)


@csrf_exempt
@login_required(login_url='signin')
def payment_page(request):
    profile = Profile.objects.get(user=request.user)
    address = Address.objects.filter(user=request.user)
    total = request.session['total']
    paypal_total = "%.2f" % (total / 70)
    razorpay_total = int(total * 100)
    context = {
        'address': address,
        'total': total,
        'paypal_total': paypal_total,
        'razorpay_total': razorpay_total,
        'profile': profile
    }
    return render(request, 'user/payment-page.html', context)


@login_required(login_url='signin')
def order_confirm(request):
    return render(request, 'user/order-confirmed.html')


@csrf_exempt
@login_required(login_url='signin')
def cancel_order(request, id):
    order = Order.objects.get(id=id)
    order.order_status = 'cancelled'
    order.save()
    return redirect('my-orders')


def confirm_order(request, id):
    order = Order.objects.get(id=id)
    order.order_status = 'confirmed'
    order.save()
    return redirect('orders')


def deliver_order(request, id):
    order = Order.objects.get(id=id)
    order.order_status = 'delivered'
    order.payment_status = True
    order.save()
    return redirect('orders')


def cancel_order_admin(request, id):
    order = Order.objects.get(id=id)
    order.order_status = 'cancelled'
    order.save()
    return redirect('orders')
