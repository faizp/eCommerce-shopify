from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User


def home(request):
    return render(request, 'admins/home.html')


def user_view(request):
    user = User.objects.all()
    context = {
        'user': user
    }
    return render(request, 'admins/user-view.html', context)


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
