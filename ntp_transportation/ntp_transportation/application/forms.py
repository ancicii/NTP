from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import User, Parcel, Train


class CreateUserForm(UserCreationForm):
    password1 = forms.Field(widget=forms.PasswordInput(attrs={'class': 'input--style-4', 'placeholder': 'Enter '
                                                                                                        'password'}))
    password2 = forms.Field(widget=forms.PasswordInput(attrs={'class': 'input--style-4', 'placeholder': 'Repeat '
                                                                                                        'password'}))
    mobile = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'input--style-4', 'placeholder': 'Enter your '
                                                                                                      'mobile phone'}))

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'username', 'password1', 'password2', 'address', 'city', 'mobile']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input--style-4', 'placeholder': 'Enter your first name'}),
            'surname': forms.TextInput(attrs={'class': 'input--style-4', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'input--style-4', 'placeholder': 'Enter your email'}),
            'username': forms.TextInput(attrs={'class': 'input--style-4', 'placeholder': 'Enter username'}),
            'address': forms.TextInput(attrs={'class': 'input--style-4', 'id': 'address'}),
            'city': forms.TextInput(attrs={'class': 'input--style-4', 'id': 'city', 'readonly': True})
        }


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input--style-4', 'placeholder': 'Enter '
                                                                                                        'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input--style-4', 'placeholder': 'Enter '
                                                                                                           'password'}))


class NewParcelForm(forms.ModelForm):
    weight = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'height:50px',
                                                            'placeholder': 'Enter weight of parcel'}))
    senderContact = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'input--style-4', 'placeholder': 'Enter '
                                                                                                             'sender\'s'
                                                                                                             'mobile '
                                                                                                             'phone'}))
    receiverContact = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'input--style-4',
                                                                     'placeholder': 'Enter receiver\'s mobile phone'}))

    class Meta:
        model = Parcel
        fields = ['destination_from', 'destination_to', 'weight', 'senderName', 'senderSurname',
                  'receiverName', 'receiverSurname', 'description', 'receiverContact', 'senderContact']
        widgets = {
            'destination_from': forms.TextInput(attrs={'id': 'start_dest'}),
            'destination_to': forms.TextInput(attrs={'id': 'end_dest'}),
            'senderName': forms.TextInput(attrs={'class': 'input--style-4', 'placeholder': 'Enter sender\'s '
                                                                                           'first name'}),
            'senderSurname': forms.TextInput(attrs={'class': 'input--style-4',
                                                    'placeholder': 'Enter sender\'s last name'}),
            'receiverName': forms.TextInput(attrs={'class': 'input--style-4',
                                                   'placeholder': 'Enter receiver\'s first name'}),
            'receiverSurname': forms.TextInput(attrs={'class': 'input--style-4',
                                                      'placeholder': 'Enter receiver\'s last name'}),
            'description': forms.TextInput(attrs={'class': 'input--style-4',
                                                  'placeholder': 'Enter description of parcel'})
        }


class NewParcelFormUser(forms.ModelForm):
    weight = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'height:50px',
                                                            'placeholder': 'Enter weight of parcel'}))
    receiverContact = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'input--style-4 receiver_contact',
                                                                     'placeholder': 'Enter receiver\'s mobile phone'}))

    class Meta:
        model = Parcel
        fields = ['destination_to', 'weight', 'receiverName', 'receiverSurname', 'description', 'receiverContact']
        widgets = {
            'destination_to': forms.TextInput(attrs={'class': 'custom-select end_dest', 'style': 'height:50px'}),
            'receiverName': forms.TextInput(attrs={'class': 'input--style-4 receiver_name',
                                                   'placeholder': 'Enter receiver\'s first name'}),
            'receiverSurname': forms.TextInput(attrs={'class': 'input--style-4 receiver_surname',
                                                      'placeholder': 'Enter receiver\'s last name'}),
            'description': forms.TextInput(attrs={'class': 'input--style-4', 'placeholder': 'Enter '
                                                                                            'description of parcel'})

        }


class NewTrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ['start_destination']
        widgets = {
            'start_destination': forms.TextInput(attrs={'class': 'input--style-4', 'id': 'start_dest'})
        }
