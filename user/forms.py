from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length= 20)
    phone_number = forms.CharField(max_length=10)
    class Meta:
        model = User
        fields = ['username','first_name','email','phone_number','password1','password2']
