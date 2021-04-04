from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from user.models import Profile
from shop.models import Category, Product, Order, Offer
from datetime import date, datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import base64
import calendar
from django.core import serializers
from django.core.files.base import ContentFile
import json
from django.contrib import messages


def home(request):
    if request.session.has_key('password'):
        # users
        users = User.objects.all().count()
        new_users = User.objects.filter(date_joined__month=datetime.now().month).count()
        active_users = User.objects.filter(is_active=True).count()
        blocked_users = User.objects.filter(is_active=False).count()
        # orders
        orders = Order.objects.all()
        orders_today = Order.objects.filter(order_date__date=date.today()).count()
        delivered_orders = Order.objects.filter(order_status='delivered').count()
        cancelled_orders = Order.objects.filter(order_status='cancelled').count()
        pending_orders = Order.objects.filter(order_status='pending').count()
        orders_month = Order.objects.filter(order_date__month=datetime.now().month)
        total = 0
        for order in orders:
            total = total + order.product.price
        income_month = 0
        for order in orders_month:
            income_month = income_month + order.product.price

        m1 = datetime.now().month
        print(m1)
        m2 = m1 - 1
        m3 = m2 - 1
        m4 = m3 - 2
        m5 = m4 - 1
        print(calendar.month_name[-1])
        print(m4, m5, m2, m3, m1)
        month1 = Order.objects.filter(order_date__month=m1).count()
        month2 = Order.objects.filter(order_date__month=m2).count()
        month3 = Order.objects.filter(order_date__month=m3).count()
        month4 = Order.objects.filter(order_date__month=m4).count()
        month5 = Order.objects.filter(order_date__month=m5).count()
        y1 = datetime.now().year
        print(y1)
        y2 = y1 - 1
        y3 = y2 - 1
        y4 = y3 - 2
        y5 = y4 - 1
        year1 = Order.objects.filter(order_date__year=y1).count()
        year2 = Order.objects.filter(order_date__year=y2).count()
        year3 = Order.objects.filter(order_date__year=y3).count()
        year4 = Order.objects.filter(order_date__year=y4).count()
        year5 = Order.objects.filter(order_date__year=y5).count()
        products = Product.objects.all().count()
        context = {
            'users': users,
            'new_users': new_users,
            'active_users': active_users,
            'blocked_users': blocked_users,
            'orders': orders.count(),
            'total': total,
            'income_month': income_month,
            'order_today': orders_today,
            'delivered_orders': delivered_orders,
            'cancelled_orders': cancelled_orders,
            'pending_orders': pending_orders,
            'products': products,
            'm1': month1, 'm2': month2, 'm3': month3, 'm4': month4, 'm5': month5,
            'first_month': calendar.month_name[m1], 'second_month': calendar.month_name[m2],
            'third_month': calendar.month_name[m3], 'fourth_month': calendar.month_name[m4],
            'fifth_month': calendar.month_name[m5],
            'y1': year1, 'y2': year2, 'y3': year3, 'y4': year4, 'y5': year5, 'y01': y1, 'y02': y2, 'y03': y3, 'y04': y4,
            'y05': y5
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
            stock = request.POST.get('product-stock')
            image1 = request.POST.get('image164')
            # format, img1 = image1.split(';base64,')
            # with open(name+'1.jpg', "wb") as fh1:
            #     fh1.write(base64.b64decode(img1))
            image2 = request.POST.get('image264')
            # format, img2 = image2.split(';base64,')
            # with open(name+'2.jpg', "wb") as fh2:
            #     fh2.write(base64.b64decode(img2))
            image3 = request.POST.get('image364')
            # format, img3 = image3.split(';base64,')
            # with open(name+'3.jpg', "wb") as fh3:
            #     fh3.write(base64.b64decode(img3))
            # ig1 = ContentFile(fh1)
            # ig2 = ContentFile(fh2)
            # ig3 = ContentFile(fh3)
            format, img1 = image1.split(';base64,')
            ext = format.split('/')[-1]
            img_data1 = ContentFile(base64.b64decode(img1), name=name + '1.' + ext)
            format, img2 = image2.split(';base64,')
            ext = format.split('/')[-1]
            img_data2 = ContentFile(base64.b64decode(img2), name=name + '2.' + ext)
            format, img3 = image3.split(';base64,')
            ext = format.split('/')[-1]
            img_data3 = ContentFile(base64.b64decode(img3), name=name + '3.' + ext)
            sub_category = request.POST.get('product-main-category')
            description = request.POST.get('product-description')
            categry = Category.objects.get(pk=p_category)
            product = Product.objects.create(category=categry, name=name, price=price, stock=stock,
                                             image1=img_data1,
                                             image2=img_data2,
                                             image3=img_data3, description=description, sec_category=sub_category)
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
            product.stock = request.POST.get('product-stock ')
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


def offers(request):
    offer = Offer.objects.all()
    context = {
        'offers': offer
    }
    return render(request, 'admins/offer.html', context)


@csrf_exempt
def add_offer(request):
    if request.method == 'POST':
        category_id = request.POST['category']
        category = Category.objects.get(pk=category_id)
        start_date = request.POST['startDate']
        end_date = request.POST['endDate']
        if Offer.objects.filter(category=category, end_date__lte=end_date).exists():
            print('exists')
            return JsonResponse('false', safe=False)
        else:
            name = request.POST['name']
            discount = request.POST['discount']

            Offer.objects.create(category = category, name = name, discount = discount, start_date = start_date, end_date = end_date)
            return JsonResponse('true', safe=False)
    else:
        category = Category.objects.all()
        context = {
            'category': category
        }
        return render(request, 'admins/add-offer.html', context)


def delete_offer(request, id):
    offer =  Offer.objects.get(id = id)
    offer.delete()
    return JsonResponse('true', safe=False)


@csrf_exempt
def monthly_report(request):
    if request.method == 'POST':
        month = request.POST['month']
        year = request.POST['year']
        user_order = Order.objects.filter(order_date__month = month, order_date__year = year)
        user_dict = {}
        product_dict = {}
        for x in user_order:
            user_dict[x.user.id] = x.user.first_name
            product_dict[x.product.id] = x.product.name
        serialized_data = serializers.serialize('json', user_order)
        # print(serialized_data)
        serialized_data = json.loads(serialized_data)
        for x in serialized_data:
            x['fields']['user_name'] = user_dict[x['fields']['user']]
            x['fields']['product_name'] = product_dict[x['fields']['product']]
        context = {
            'user_order': json.dumps(serialized_data)
        }
        return JsonResponse(context)
    #     return render(request, 'admins/report.html', context)
    # else:

    #     return render(request, 'admins/report.html', {'user_order': book})
    # return render(request, 'admins/report.html', context)


def report(request):
    today = date.today()
    week = date.today() - timedelta(days=7)
    book = Order.objects.filter(order_date__range=(week, today))
    context = {
        'order': book
    }
    return render(request, 'admins/report.html', context)


def report_date_range(request):
    context = {}
    if request.method == 'POST':
        start_date = request.POST.get('date-start')
        end_date = request.POST.get('date-end')
        print(start_date, end_date)
        order = Order.objects.filter(order_date__range=[start_date, end_date])
        if len(order) < 1:
            messages.error(request, "There is no orders in selected dates")
            return redirect('report-date-range')
        context = {'order': order}
    return render(request, 'admins/report-daily.html', context)
