from django.urls import path

from . import views

# NOTE: only one views per url

urlpatterns = [
    path('', views.home, name='homepage'),
    # The about page view
    path('about/', views.aboutus, name='about'),
    # The Privacy policy page
    path('privacy_policy/', views.privacy_policy, name='privacy-policy'),
    # terms and conditions
    path('terms_and_conditions/', views.terms_and_conditions,
         name='terms-and-conditions'),
]
