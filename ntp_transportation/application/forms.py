from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User, Parcel, Train, Destination


class CreateUserForm(UserCreationForm):
    password1 = forms.Field(widget=forms.PasswordInput(attrs={'class': 'input--style-4'}))
    password2 = forms.Field(widget=forms.PasswordInput(attrs={'class': 'input--style-4'}))

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


class NewParcelForm(forms.ModelForm):
    weight = forms.FloatField(widget=forms.TextInput(attrs={'class': 'input--style-4'}))
    price = forms.FloatField(widget=forms.TextInput(attrs={'class': 'input--style-4'}))

    class Meta:
        model = Parcel
        fields = ['destination_from', 'destination_to', 'weight', 'price']
        widgets = {
            'destination_from': forms.Select(attrs={'class': 'custom-select'}),
            'destination_to': forms.Select(attrs={'class': 'custom-select'}),
        }


class NewDestinationForm(forms.ModelForm):
    zipcode = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'input--style-4'}))
    latitude = forms.FloatField(widget=forms.TextInput(attrs={'class': 'input--style-4'}))
    longitude = forms.FloatField(widget=forms.TextInput(attrs={'class': 'input--style-4'}))

    class Meta:
        model = Destination
        fields = ['name', 'country', 'zipcode', 'state', 'longitude', 'latitude']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input--style-4'}),
            'country': forms.TextInput(attrs={'class': 'input--style-4'}),
            'state': forms.TextInput(attrs={'class': 'input--style-4'}),
        }


class NewTrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ['start_destination']
        widgets = {
            'start_destination': forms.Select(attrs={'class': 'custom-select'})
        }
