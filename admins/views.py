from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from shop.models import Category
from shop.models import Product
from django.views.decorators.csrf import csrf_exempt


def home(request):
    if request.session.has_key('password'):
        return render(request, 'admins/home.html')
    else:
        return redirect(admin_login)


def user_view(request):
    if request.session.has_key('password'):
        user = User.objects.all()
        context = {
            'user': user
        }
        return render(request, 'admins/user-view.html', context)
    else:
        return redirect(admin_login)


def admin_login(request):
    if request.session.has_key('password'):
        return redirect(home)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            if username == 'admin' and password == 'admin':
                request.session['password'] = password
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe = False)
        else:
            return render(request, 'admins/login.html')


def admin_logout(request):
    if request.session.has_key('password'):
        request.session.flush()
        return redirect(admin_login)


def product_view(request):
    if request.session.has_key('password'):
        products = Product.objects.all()
        return render(request, 'admins/product-view.html', {'products': products})

@csrf_exempt
def add_product(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            p_category = request.POST.get('product-category')
            name = request.POST.get('product-name')
            price = request.POST.get('product-price')
            image1 = request.POST.get('image1')
            image2 = request.POST.get('image2')
            image3 = request.POST.get('image3')
            sub_category = request.POST.get('product-main-category')
            description = request.POST.get('product-description')
            # print(description)
            categry = Category.objects.get(pk=p_category)
            product = Product.objects.create(category=categry,name=name,price=price,image1=image1,image2=image2,image3=image3,description=description,sec_category=sub_category)
            product.save()
            return redirect(home)
        else:
            category = Category.objects.all()
            return render(request, 'admins/add-product.html', {'category':category})
    else:
        return redirect(admin_login)