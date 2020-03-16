from django.urls import include, path

from .views import newsletter_signup, newsletter_unsubscribe, control_newsletter

urlpatterns = [
    path('subscribe/', newsletter_signup, name="newsletter_signup"),
    path('unsubscribe/',newsletter_unsubscribe, name= "newsletter_unsubscribe"),
    path('control/',control_newsletter, name="control")
    
]
