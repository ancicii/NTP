from django.forms import  ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User


class CreateUserForm(UserCreationForm):
        password1 = forms.Field(widget=forms.PasswordInput(attrs={'class':'input--style-4'}))
        password2 = forms.Field(widget=forms.PasswordInput(attrs={'class':'input--style-4'}))
        class Meta:
            model = User
            fields = ['name', 'surname', 'email', 'username', 'password1', 'password2', 'address', 'city']
            widgets = {
            'name': forms.TextInput(attrs={'class': 'input--style-4'}),
            'surname': forms.TextInput(attrs={'class': 'input--style-4'}),
            'email': forms.EmailInput(attrs={'class': 'input--style-4'}),
            'username': forms.TextInput(attrs={'class': 'input--style-4'}),
            'address': forms.TextInput(attrs={'class': 'input--style-4'}),
            'city': forms.TextInput(attrs={'class': 'input--style-4'}),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input--style-4'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input--style-4'}))
