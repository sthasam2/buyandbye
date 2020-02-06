from django.contrib.auth import views as auth_views
from django.urls import include, path

from users import views as user_views

urlpatterns = [
    # profile
    path('profile/', user_views.profile, name='profile'),
    path('profile/update/', user_views.profile_update, name='profile_update'),

    # forms
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # password forms
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'),
         name='password_reset'),  # reset form

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),  # reset token link

    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),  # reset email link generator

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),  # password reset route displays success message

    # account activation via email
    path('register/activate/<slug:uidb64>/<slug:token>/',
         user_views.activate, name='activate')
]
