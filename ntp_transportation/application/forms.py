from django.forms import  ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class CreateUserForm(UserCreationForm):
        password1 = forms.Field(widget=forms.PasswordInput(attrs={'class':'input--style-4'}))
        password2 = forms.Field(widget=forms.PasswordInput(attrs={'class':'input--style-4'}))
        class Meta:
            model = User
            fields = ['name', 'surname', 'email', 'username', 'password1', 'password2']
            widgets = {
            'name': forms.TextInput(attrs={'class': 'input--style-4'}),
            'surname': forms.TextInput(attrs={'class': 'input--style-4'}),
            'email': forms.EmailInput(attrs={'class': 'input--style-4'}),
            'username': forms.TextInput(attrs={'class': 'input--style-4'}),
        }
