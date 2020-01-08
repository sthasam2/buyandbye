from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from . models import Profile


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Given name'}))
    middle_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Middle name'}))
    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
    email = forms.EmailField(
        max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    address1 = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Street, District'}))
    address2 = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'State'}))
    phone = PhoneNumberField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'username',
                  'email', 'phone', 'password1', 'password2', 'address1', 'address2']


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Given name'}))
    middle_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Middle name'}))
    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
    email = forms.EmailField(
        max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    address1 = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Street, District'}))
    address2 = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'State'}))
    phone = PhoneNumberField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'e.g. +97798XXYYZZSS'}))

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'username',
                  'email', 'phone', 'address1', 'address2']
        widget={
            User.username: forms.TextInput(attrs={'placeholder': 'Enter desired username.'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        # wigets = {
        #  image: form.TextInput(attrs={'placeholder': 'Choose an image for the item'})
        # }
