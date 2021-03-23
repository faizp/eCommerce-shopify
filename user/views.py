from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, Address
import requests, json
from shop.models import Product, Order, Size, Offer
from django.contrib.auth import login, authenticate, logout
from datetime import date


def index(request):
    products = Product.objects.all()
    size = Size.objects.all()
    for product in products:
        offer = Offer.objects.filter(category=product.category, valid=True)
        if offer.exists():
            if offer[0].start_date <= date.today() <= offer[0].end_date:
                offer[0].valid = True
                product.offerPrice = product.price - (product.price*offer[0].discount)/100
            else:
                offer[0].valid = False
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
                print(user)
                login(request, user)
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


def addresses(request):
    user = request.user
    address = Address.objects.filter(user=user)
    context = {
        'address': address
    }
    return render(request, 'user/addresses.html', context)


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


def delete_address(request, id):
    address = Address.objects.get(id=id)
    address.delete()
    return redirect('user-addresses')


def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'user/profile.html', {'profile': profile})


def logout_user(request):
    logout(request)
    return redirect(index)


def register_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            image = request.FILES.get('image')
            phone = request.POST.get('phone')
            Profile.objects.create(user = user, image = image, phone_num = phone)
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
                print(request.session['otp_id'])
                print(response.text.encode('utf8'))
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
            print(otp)
            print(phone)
            profile = Profile.objects.get(phone_num=phone)
            user = User.objects.get(id=profile.id)
            otp_id = request.session['otp_id']
            print(otp_id)
            payload = {'otp_id': otp_id, 'otp_code': otp}
            files = [
            ]
            headers = {
                'Authorization': 'Token de1422343677e30e08c10f633afde0954a576fcd'
            }
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            print(response.text.encode('utf8'))
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
    # if request.session.has_key('otp_id_signup'):
    #     phone = request.session['phone_signup']
    #     context = {'phone': phone}
    #     return render(request, 'user/otp-login.html', context)


def my_orders(request):
    orders = Order.objects.filter(user = request.user)
    context = {
        'orders': orders
    }
    return render(request, 'user/my-orders.html', context)