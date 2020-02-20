from django.urls import path, include
from .views import newsletter_signup, newsletter_unsubscribe


urlpatterns = [
    path('subscribe/', newsletter_signup, name="newsletter_signup"),
    path('unsubscribe/',newsletter_unsubscribe, name= "newsletter_unsubscribe"),
    
]
