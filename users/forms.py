from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import CountryField
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(help_text="xxx@gmail.com")
    phone = PhoneNumberField(required=False, help_text="e.g. +97798XXYYYYYY")
    first_name = forms.CharField(
        max_length=30, required=True, help_text='First Name')
    middle_name = forms.CharField(
        max_length=30, required=False, help_text='Middle Name')
    last_name = forms.CharField(
        max_length=30, required=True, help_text='Last Name')
    country = CountryField(blank_text='Country Name')
    address = forms.TextField(help_text='Street, District, State')

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'username',
                  'email', 'phone', 'password1', 'password2', 'country', 'address']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    phone = PhoneNumberField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
