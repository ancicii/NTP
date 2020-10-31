from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import User, Parcel, Train


class CreateUserForm(UserCreationForm):
    password1 = forms.Field(widget=forms.PasswordInput(attrs={'class': 'input--style-4'}))
    password2 = forms.Field(widget=forms.PasswordInput(attrs={'class': 'input--style-4'}))
    mobile = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'input--style-4'}))

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'username', 'password1', 'password2', 'address', 'city', 'mobile']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input--style-4'}),
            'surname': forms.TextInput(attrs={'class': 'input--style-4'}),
            'email': forms.EmailInput(attrs={'class': 'input--style-4'}),
            'username': forms.TextInput(attrs={'class': 'input--style-4'}),
            'address': forms.TextInput(attrs={'class': 'input--style-4', 'id': 'address'}),
            'city': forms.TextInput(attrs={'class': 'input--style-4', 'id': 'city', 'readonly': True})
        }


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input--style-4'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input--style-4'}))


class NewParcelForm(forms.ModelForm):
    weight = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    senderContact = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'input--style-4'}))
    receiverContact = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'input--style-4'}))

    class Meta:
        model = Parcel
        fields = ['destination_from', 'destination_to', 'weight', 'senderName', 'senderSurname',
                  'receiverName', 'receiverSurname', 'description', 'receiverContact', 'senderContact']
        widgets = {
            'destination_from': forms.TextInput(attrs={'class': 'custom-select', 'id': 'start_dest'}),
            'destination_to': forms.TextInput(attrs={'class': 'custom-select', 'id': 'end_dest'}),
            'senderName': forms.TextInput(attrs={'class': 'input--style-4'}),
            'senderSurname': forms.TextInput(attrs={'class': 'input--style-4'}),
            'receiverName': forms.TextInput(attrs={'class': 'input--style-4'}),
            'receiverSurname': forms.TextInput(attrs={'class': 'input--style-4'}),
            'description': forms.TextInput(attrs={'class': 'input--style-4'})
        }


class NewParcelFormUser(forms.ModelForm):
    weight = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    receiverContact = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'input--style-4 receiver_contact'}))

    class Meta:
        model = Parcel
        fields = ['destination_to', 'weight', 'receiverName', 'receiverSurname', 'description', 'receiverContact']
        widgets = {
            'destination_to': forms.TextInput(attrs={'class': 'custom-select end_dest'}),
            'receiverName': forms.TextInput(attrs={'class': 'input--style-4 receiver_name'}),
            'receiverSurname': forms.TextInput(attrs={'class': 'input--style-4 receiver_surname'}),
            'description': forms.TextInput(attrs={'class': 'input--style-4'})

        }


class NewTrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ['start_destination']
        widgets = {
            'start_destination': forms.TextInput(attrs={'class': 'input--style-4', 'id': 'start_dest'})
        }
