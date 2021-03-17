from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from user.models import Profile
from shop.models import Category, Product, Order
from datetime import date
from django.views.decorators.csrf import csrf_exempt


def home(request):
    if request.session.has_key('password'):
        users = len(User.objects.all())
        orders = Order.objects.all()
        total = 0
        print(date.today())
        orders_today = Order.objects.filter(order_date__date = date.today()).count()
        for order in orders:
            total = total + order.product.price
        context = {
            'users': users,
            'order_len': len(orders),
            'total': total,
            'order_today': orders_today
        }
        return render(request, 'admins/dashboard.html', context)
    else:
        return redirect('admin-login')


def user_view(request):
    if request.session.has_key('password'):
        # user = User.objects.all()
        profile = Profile.objects.all()
        print(profile)
        context = {
            # 'user': user,
            'profile': profile
        }
        return render(request, 'admins/user-view.html', context)
    else:
        return redirect('admin-login')


def admin_login(request):
    if request.session.has_key('password'):
        return redirect('admin-home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            if username == 'admin' and password == 'admin':
                request.session['password'] = password
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return render(request, 'admins/login.html')


def admin_logout(request):
    if request.session.has_key('password'):
        request.session.flush()
        return redirect('admin-login')


def product_view(request):
    if request.session.has_key('password'):
        products = Product.objects.all()
        return render(request, 'admins/product-view.html', {'products': products})
    else:
        return redirect('admin-login')


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
            sub_category = request.POST.get('product-main-category')
            description = request.POST.get('product-description')
            categry = Category.objects.get(pk=p_category)
            product = Product.objects.create(category=categry, name=name, price=price, image1=image1, image2=image2,
                                             image3=image3, description=description, sec_category=sub_category)
            product.save()
            return redirect('admin-home')
        else:
            category = Category.objects.all()
            return render(request, 'admins/add-product.html', {'category': category})
    else:
        return redirect('admin-login')


def block_user(request, id):
    user = User.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('user-view')


def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('product-view')


def edit_user(request, id):
    if request.session.has_key('password'):
        if request.method == 'POST':
            user = User.objects.get(id=id)
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.first_name = request.POST.get('first-name')
            user.last_name = request.POST.get('last-name')
            user.save()
            return redirect(user_view)
        else:
            user = User.objects.get(id=id)
            return render(request, 'admins/edit.html', {'user': user})
    else:
        return redirect('admin-login')


def edit_product(request, id):
    if request.session.has_key('password'):
        if request.method == 'POST':
            product = Product.objects.get(id=id)
            p_category = request.POST.get('product-category')
            categry = Category.objects.get(pk=p_category)
            product.category = categry
            product.name = request.POST.get('product-name')
            product.price = request.POST.get('product-price')
            product.image1 = request.FILES.get('image1')
            product.image2 = request.FILES.get('image2')
            product.image3 = request.FILES.get('image3')
            product.sec_category = request.POST.get('product-main-category')
            product.description = request.POST.get('description')
            product.save()
            return redirect('product-view')

        else:
            category = Category.objects.all()
            product = Product.objects.get(id=id)
            context = {
                'product': product,
                'category': category
            }
            return render(request, 'admins/edit-product.html', context)
    else:
        return redirect('admin-login')


def category(request):
    if request.session.has_key('password'):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'admins/category.html', context)
    else:
        return redirect('admin-login')


@csrf_exempt
def add_category(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            name = request.POST['category']
            if Category.objects.filter(name=name).exists():
                return JsonResponse('false', safe=False)
            else:
                Category.objects.create(name=name)
                return JsonResponse('true', safe=False)
        else:
            return render(request, 'admins/add-category.html')
    else:
        return redirect('admin-login')


def delete_category(request, id):
    if request.session.has_key('password'):
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('categories')


@csrf_exempt
def edit_category(request, id):
    if request.session.has_key('password'):
        if request.method == 'POST':
            category = Category.objects.get(id=id)
            category.name = request.POST.get('category-name')
            category.save()
            return redirect('categories')
        else:
            category = Category.objects.get(id=id)
            return render(request, 'admins/edit-category.html', {'category': category})
    else:
        return redirect('admin-login')


def orders(request):
    order = Order.objects.all()
    context = {
        'order': order
    }
    return render(request, 'admins/order.html', context)


