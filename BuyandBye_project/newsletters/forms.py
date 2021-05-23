from crispy_forms.helper import FormHelper
from django import forms

from .models import NewsLetter, NewsletterUser


class NewsletterSignUpForm(forms.ModelForm):
    class Meta:
        model = NewsletterUser
        fields = ["email"]

        def clean_email(self):
            email = self.cleaned_data.get("email")

            return email


class NewsletterCreationForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = (
            "subject",
            "body",
            "email",
            "status",
        )
