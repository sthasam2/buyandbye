from django.contrib import messages  # for message tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# for site domain e.g. 127.00:8000
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import (ProfileUpdateForm, UserRegisterForm,  # profile forms
                    UserUpdateForm)
from .utils import account_activation_token  # token variable


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():  # form validity checker (returns different kinds of error if not valid like weak password, etc)
            user = form.save()
            user.is_active = False
            user.save()

            # save different form data
            # username = form.cleaned_data.get('username')
            # first_name = form.cleaned_data.get('first_name')
            # middle_name = form.cleaned_data.get('middle_name')
            # last_name = form.cleaned_data.get('last_name')
            # phone = form.cleaned_data.get('phone')
            to_email = form.cleaned_data.get('email')

            # email info and content generater
            current_site = get_current_site(request)  # site getter
            mail_subject = 'Account activation.'  # subject
            message = render_to_string('users/register/account_activation_email.html', {  # message content
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })

            # email sender
            activation_email = EmailMessage(
                mail_subject, message, to=[to_email])
            activation_email.send()

            # return redirect('activation_message_sent')
            # email send success info message
            messages.info(
                request, f'Your account has been created! An email has been sent with instructions, Please verify your email to login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register/register.html', {'form': form})


# def activation_message_sent(request):
#     return render(request, 'users/register/account_activate_message.html', {'title': 'Activate email'})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        username = user.username
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(
            request, f'{username}, Your email has been validated! Now you can login.')
        return redirect('login')
    else:
        return render(request, 'users/register/account_activation_unvalidated.html')


@login_required
def profile(request):
    return render(request, 'users/profile/profile.html')


@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been updated, {username}!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile/profile_update.html', context)
