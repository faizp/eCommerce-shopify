from django.shortcuts import render, redirect
from django.http import JsonResponse
from . forms import UserRegisterForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, Address
from shop.models import Product
from django.contrib.auth import login, authenticate, logout


def index(request):
    products = Product.objects.all()
    return render(request, 'user/home.html', {'product': products})


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(index)
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
            user = authenticate(request, username = username, password = password)
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
    address = Address.objects.filter(user = user)
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
        Address.objects.create(user = user, house_name = house_name, town = town, district = district, state = state, pin_code = pin_code, type = address_type)
        return redirect('user-addresses')


def edit_address(request, id):
    address = Address.objects.get(id = id)
    print(address)
    address.house_name = request.POST.get('house-name')
    address.town = request.POST.get('town')
    address.district = request.POST.get('district')
    address.state = request.POST.get('state')
    address.pin_code = request.POST['pin-code']
    address.address_type = request.POST.get('address-type')
    address.save()
    return redirect('user-addresses')


def delete_address(request, id):
    address = Address.objects.get(id = id)
    address.delete()
    return redirect('user-addresses')


def profile(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    return render(request, 'user/profile.html', {'profile':profile})



def logout_user(request):
    logout(request)
    return redirect(index)

