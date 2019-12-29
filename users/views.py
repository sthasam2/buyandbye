from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError  # for site domain e.g. 127.00:8000
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages  # for message tags
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .tokens import account_activation_token  # token variable
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm  # profile forms


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profie.first_name = form.cleaned_data.get('first_name')
            user.profie.middle_name = form.cleaned_data.get('middle_name')
            user.profie.last_name = form.cleaned_data.get('last_name')
            user.profie.email = form.cleaned_data.get('email')
            user.profie.phone = form.cleaned_data.get('phone')
            # login disabled until confirmation
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate you account.'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                mail_subject, message, to=[user.profie.email]
            )
            email.send()

            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for {username}! Please check your email to activate your account to login.')
            return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
        messages.success(
            request, f'Congratulations, account for {username} activated! You can now successfully login.')
    else:
        return render(request, 'users/account_activation_unvalidated.html' )


@login_required
def profile(request):
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
    return render(request, 'users/profile.html', context)
