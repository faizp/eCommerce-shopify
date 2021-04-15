from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, Address
import requests, json, uuid
from shop.models import Product, Order, Size, Offer, Category, Coupon
from django.contrib.auth import login, authenticate, logout
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    products = Product.objects.all()
    size = Size.objects.all()
    for product in products:
        offer = Offer.objects.filter(category=product.category, start_date__lte=date.today(),
                                     end_date__gte=date.today()).first()
        if offer is not None:
            product.offerPrice = product.price - (product.price * offer.discount) / 100
        else:
            product.offerPrice = product.price
    context = {
        'product': products,
        'size': size
    }
    return render(request, 'user/user-home.html', context)


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                refer = uuid.uuid4().hex[:6].upper()
                Coupon.objects.create(code='WELCOME50', discount=50, user=user)
                Profile.objects.create(user=user, refer=refer)
                return redirect('register-user')
        else:
            form = UserRegisterForm()
        return render(request, 'user/register.html', {"form": form})
    else:
        return redirect(index)


def register_refer(request,uid):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                refer = uuid.uuid4().hex[:6].upper()
                Profile.objects.create(user=user, refer=refer, refer_by=uid)
                Coupon.objects.create(code='WELCOME50', discount=50, user=user)
                user = Profile.objects.get(refer=uid).user
                Coupon.objects.create(code='RFR30', discount=30, user=user)
                return redirect('register-user')
        else:
            form = UserRegisterForm()
        return render(request, 'user/register.html', {"form": form})
    else:
        return redirect(index)


@csrf_exempt
def login_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return render(request, 'user/login.html')
    else:
        return redirect(index)


@login_required(login_url='signin')
def addresses(request):
    user = request.user
    address = Address.objects.filter(user=user)
    context = {
        'address': address
    }
    return render(request, 'user/addresses.html', context)


@login_required(login_url='signin')
def add_new_address(request):
    user = request.user
    if request.method == 'POST':
        house_name = request.POST.get('house-name')
        town = request.POST.get('town')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pin_code = request.POST['pin-code']
        address_type = request.POST.get('address-type')
        Address.objects.create(user=user, house_name=house_name, town=town, district=district, state=state,
                               pin_code=pin_code, type=address_type)
        return redirect('user-addresses')


@login_required(login_url='signin')
def add_new_address_checkout(request):
    user = request.user
    if request.method == 'POST':
        house_name = request.POST.get('house-name')
        town = request.POST.get('town')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pin_code = request.POST['pin-code']
        address_type = request.POST.get('address-type')
        Address.objects.create(user=user, house_name=house_name, town=town, district=district, state=state,
                               pin_code=pin_code, type=address_type)
        return redirect('payment-page')


@login_required(login_url='signin')
def edit_address(request, id):
    address = Address.objects.get(id=id)
    address.house_name = request.POST.get('house-name')
    address.town = request.POST.get('town')
    address.district = request.POST.get('district')
    address.state = request.POST.get('state')
    address.pin_code = request.POST['pin-code']
    address.address_type = request.POST.get('address-type')
    address.save()
    return redirect('user-addresses')


@login_required(login_url='signin')
def delete_address(request, id):
    address = Address.objects.get(id=id)
    address.delete()
    return redirect('user-addresses')


@login_required(login_url='signin')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'user/profile.html', {'profile': profile})


def logout_user(request):
    logout(request)
    return redirect(index)


def register_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            profile = Profile.objects.get(user=request.user)
            image = request.FILES.get('image')
            phone_num = request.POST.get('phone')
            if Profile.objects.filter(phone_num=phone_num).exists():
                messages.error(request, "This Phone number is already registered! Try using a different Phone number.")
                return redirect('register-user')
            profile.image = image
            profile.phone_num = phone_num
            profile.save()
            return redirect('index')
        else:
            return render(request, 'user/register_user.html')
    else:
        return redirect('login')


def phone(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            phone = request.POST.get('phone')
            if Profile.objects.filter(phone_num=phone).exists():
                request.session['phone'] = phone
                url = "https://d7networks.com/api/verifier/send"
                phone1 = '91' + str(phone)
                payload = {'mobile': phone1,
                           'sender_id': 'SMSINFO',
                           'message': 'Your Shopify login verification code is {code}',
                           'expiry': '900'}
                files = [
                ]
                headers = {
                    'Authorization': 'Token de1422343677e30e08c10f633afde0954a576fcd'
                }
                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                data = response.text.encode('utf8')
                dict = json.loads(data.decode('utf8'))
                otp_id = dict["otp_id"]
                request.session['otp_id'] = otp_id
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return render(request, 'user/otp-login.html')
    else:
        return redirect('index')


def otp_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            phone = request.session['phone']
            url = "https://d7networks.com/api/verifier/verify"
            otp = request.POST['otp']
            profile = Profile.objects.get(phone_num=phone)
            user = User.objects.get(id=profile.id)
            otp_id = request.session['otp_id']
            payload = {'otp_id': otp_id, 'otp_code': otp}
            files = [
            ]
            headers = {
                'Authorization': 'Token de1422343677e30e08c10f633afde0954a576fcd'
            }
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            data = response.text.encode('utf8')
            dict = json.loads(data.decode('utf8'))
            status = dict['status']
            if status == 'success':
                login(request, user)
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return redirect('otp-login')
    else:
        return redirect('index')


@login_required(login_url='signin')
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, 'user/my-orders.html', context)


def about(request):
    return render(request, 'user/about.html')


def contact(request):
    return render(request, 'user/contact.html')


def change_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        user = Profile.objects.get(user=request.user)
        user.image = image
        user.save()
    return redirect('user-profile')


def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('search')
        category = Category.objects.filter(name__icontains=keyword)
        if len(category) == 0:
            return render(request, 'user/product.html')
        products = Product.objects.filter(category=category[0])
        size = Size.objects.all()
        for product in products:
            offer = Offer.objects.filter(category=product.category, start_date__lte=date.today(),
                                         end_date__gte=date.today()).first()
            if offer is not None:
                product.offerPrice = product.price - (product.price * offer.discount) / 100
            else:
                product.offerPrice = product.price
        context = {
            'product': products,
            'size': size
        }
        return render(request, 'user/product.html', context)
    return redirect('index')


def edit_profile(request, id):
    user_profile = Profile.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    user.username = request.POST.get('username')
    user.email = request.POST.get('email')
    user.first_name = request.POST.get('first-name')
    user.last_name = request.POST.get('last-name')
    user_profile.phone_num = request.POST.get('phone-number')
    user.save()
    user_profile.save()
    return redirect('user-profile')


def apply_coupon(request):
    code = request.POST['code']
    if Coupon.objects.filter(code=code).exists():
        coupon = Coupon.objects.get(code=code)
        total = request.session['total']
        request.session['coupon'] = coupon.id
        discount = total - (total * coupon.discount) / 100
        request.session['discount'] = discount
        amount_deducted = total - discount
        context = {
            'total': "%.2f" % discount,
            'code': code,
            'amount': "%.2f" % amount_deducted
        }
        return JsonResponse(context)
    return JsonResponse('false', safe=False)
