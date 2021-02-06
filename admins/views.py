from django.shortcuts import render
from django.contrib.auth.models import User


def home(request):
    return render(request, 'admins/home.html')


def user_view(request):
    user = User.objects.all()
    context = {
        'user': user
    }
    return render(request, 'admins/user-view.html', context)