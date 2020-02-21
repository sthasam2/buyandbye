from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import render
from django.template.loader import get_template

from .forms import NewsletterCreationForm, NewsletterSignUpForm
from .models import NewsLetter, NewsletterUser


def newsletter_signup(request):
    form = NewsletterSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            messages.warning(request, 'This email exists already in our database',
                             "alert alert-warning alert-dismissible")
        else:
            instance.save()
            messages.success(
                request, 'You have Subscribed to our Newsletter Service. Your email has been added to our database')
            subject = "Thank you for joining our Newsletter"
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            with open(settings.BASE_DIR + "/templates/newsletters/subscribe_email.txt") as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(
                subject=subject, body=signup_message, from_email=from_email, to=to_email)
            html_template = get_template(
                "newsletters/subscribe_email.html").render()
            message.attach_alternative(html_template, "text/html")
            message.send()
    context = {
        "form": form,
    }

    template = "newsletters/subscribe.html"
    return render(request, template, context)


def newsletter_unsubscribe(request):
    form = NewsletterSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.success(request, 'Your email has been deleted from our database.',
                             "alert alert-success alert-dismissible")
            subject = "You have been unsubscribed"
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            with open(settings.BASE_DIR + "/templates/newsletters/unsubscribe_email.txt") as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(
                subject=subject, body=signup_message, from_email=from_email, to=to_email)
            html_template = get_template(
                "newsletters/unsubscribe_email.html").render()
            message.attach_alternative(html_template, "text/html")
            message.send()
        else:
            messages.warning(request, 'We dont have the email you entered in our database',
                             "alert alert-warning alert-dismissible")

    context = {
        "form": form,
    }

    template = "newsletters/unsubscribe.html"
    return render(request, template, context)


def control_newsletter(request):
    form = NewsletterCreationForm(request.POST or None)

    if form.is_valid():
        instance = form.save()
        newsletter = NewsLetter.objects.get(id=instance.id)
        if newsletter.status == "Published":
            subject = newsletter.subject
            body = newsletter.body
            from_email = settings.EMAIL_HOST_USER
            for email in newsletter.email.all():
                print(email)
                send_mail(subject=subject, from_email=from_email, recipient_list=[
                          email.email], message=body, fail_silently=True)

    context = {
        'form': form,
    }

    template = "newsletters/control_newsletter.html"
    return render(request, template, context)
