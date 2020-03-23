from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

from .models import Profile
from .options import STATE_CHOICES, YEARS
from .utils import AgeValidator


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Given name'}))
    middle_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Middle name'}))
    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
    date_of_birth = forms.DateField(label='Date of Birth', initial=date.today(),
                                    required=True, help_text='Age must be above 16', validators=[AgeValidator], widget=forms.SelectDateWidget(years=YEARS))
    email = forms.EmailField(
        max_length=150, widget=forms.TextInput(attrs={'placeholder': 'e.g. xyz@domain.com'}))
    address1 = forms.CharField(max_length=100, help_text='Street, District', widget=forms.TextInput(
        attrs={'placeholder': 'Street, District'}))
    address2 = forms.CharField(max_length=100, help_text='State', widget=forms.Select(
        attrs={'placeholder': 'State'}, choices=STATE_CHOICES))
    phone = PhoneNumberField(required=False, initial='+977',
                             help_text='Phone number must contain country calling code (e.g. +97798XXYYZZSS)')

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'date_of_birth', 'username',
                  'email', 'phone', 'password1', 'password2', 'address1', 'address2']
        # widget={
        #     'username': forms.TextInput(attrs={'placeholder': 'Enter desired username.'}),
        # }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
        ]


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Given name'}))
    middle_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Middle name'}))
    last_name = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
    email = forms.EmailField(
        max_length=150, widget=forms.TextInput(attrs={'placeholder': 'e.g. xyz@domain.com'}))
    address1 = forms.CharField(max_length=100, help_text='Street, District', widget=forms.TextInput(
        attrs={'placeholder': 'Street, District'}))
    address2 = forms.CharField(max_length=100, help_text='State', widget=forms.Select(
        attrs={'placeholder': 'State'}, choices=STATE_CHOICES))
    phone = PhoneNumberField(required=False,
                             help_text='Phone number must contain country calling code (e.g. +97798XXYYZZSS)')

    class Meta:
        model = Profile
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'address1', 'address2', 'phone', 'image']
