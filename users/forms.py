from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from . models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = PhoneNumberField(required=False)
    first_name = forms.CharField(
        max_length=30)
    middle_name = forms.CharField(
        max_length=30)
    last_name = forms.CharField(
        max_length=30)
    address = forms.CharField(help_text='Street, District, State')

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'username',
                  'email', 'phone', 'password1', 'password2', 'address']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    phone = PhoneNumberField(required=False)
    first_name = forms.CharField(
        max_length=30)
    middle_name = forms.CharField(
        max_length=30, required=False)
    last_name = forms.CharField(
        max_length=30)
    address = forms.CharField(help_text='Street, District, State')

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'username',
                  'email', 'phone', 'address']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
