from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import NewsletterUser
from .forms import NewsletterSignUpForm
from django.conf import settings
from django.template.loader import get_template
# Create your views here.


def newsletter_signup(request):
    form = NewsletterSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email = instance.email).exists():
            messages.warning(request,'This email exists already in our database', "alert alert-warning alert-dismissible")
        else:
            instance.save()
            messages.success(request, 'You have Subscribed to our Newsletter Service. Your email has been added to our database')
            subject = "Thank you for joining our Newsletter"
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            with open(settings.BASE_DIR + "/templates/newsletters/subscribe_email.txt") as f:
                signup_messege = f.read()
            message = EmailMultiAlternatives(subject=subject, body= signup_messege, from_email=from_email, to=to_email)
            html_template = get_template("newsletters/subscribe_email.html").render()
            message.attach_alternative(html_template, "text/html")
    context = {
        "form" : form,
    }    

    template = "newsletters/subscribe.html"
    return render(request, template, context)
    

def newsletter_unsubscribe(request):
    form = NewsletterSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.success(request,'Your email has been deleted from our database.', "alert alert-success alert-dismissible")
            subject = "You have been unsubscribed"
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            signup_message = "Sorry to know. Let us know if you have any issues."
            send_mail(subject=subject, from_email=from_email, recipient_list=to_email, message=signup_message, fail_silently=False)
        else:
            messages.warning(request, 'We dont have the email you entered in our database', "alert alert-warning alert-dismissible")

    context = {
        "form" : form,
    }    

    template = "newsletters/unsubscribe.html"
    return render(request, template, context)

