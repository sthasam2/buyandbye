from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = PhoneNumberField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

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