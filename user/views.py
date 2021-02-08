from django.shortcuts import render, redirect
from django.http import JsonResponse
from . forms import UserRegisterForm
from django.contrib.auth.models import User
from shop.models import Product
from django.contrib.auth import login, authenticate, logout


def index(request):
    products = Product.objects.all()
    return render(request, 'user/home.html', {'product': products})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(index)
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {"form": form})


def login(request):
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


def logout(request):
    logout(request)
    return redirect(login)