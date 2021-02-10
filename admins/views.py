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
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')
            # print(image3.url,image2,image1)
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

def delete_user(request,id):
    user = User.objects.get(id = id)
    user.delete()
    return redirect(user_view)

def delete_product(request,id):
    product = Product.objects.get(id = id)
    product.delete()
    return redirect(product_view)


def edit_user(request,id):
    if request.session.has_key('password'):
        if request.method == 'POST':
            user = User.objects.get(id = id)
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.first_name = request.POST.get('first-name')
            user.last_name = request.POST.get('last-name')
            user.save()
            return redirect(user_view)
        else:
            user = User.objects.get(id = id)
            return render(request, 'admins/edit.html', {'user':user})
    else:
        return redirect(admin_login)


def edit_product(request,id):
    if request.session.has_key('password'):
        if request.method == 'POST':
            product = Product.objects.get(id = id)
            p_category = request.POST.get('product-category')
            categry = Category.objects.get(pk=p_category)
            product.category = categry
            product.name = request.POST.get('product-name')
            product.price = request.POST.get('product-price')
            product.image1 = request.FILES.get('image1')
            product.image2 = request.FILES.get('image2')
            product.image3 = request.FILES.get('image3')
            print(product.image1)
            product.sec_category = request.POST.get('product-main-category')
            product.description = request.POST.get('description')
            product.save()
            return redirect(product_view)

        else:
            category = Category.objects.all()
            product = Product.objects.get(id = id)
            context = {
                'product':product,
                'category':category
            }
            return render(request, 'admins/edit-product.html', context)
    else:
        return redirect(admin_login)
