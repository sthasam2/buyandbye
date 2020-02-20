from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from users import views as user_views

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # homepage
    path('', include('homepage.urls')),

    # users
    path('', include('users.urls')),

    # newsletter
    path('newsletter/', include(('newsletters.urls',
                                 'newsletters'), namespace='newsletter')),

    # hit count requirement
    # django 3.0 doesnt support python_2_unicode so remove import and decorator from hitcount source file model
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),

    # all auth requirement
    path('accounts/', include('allauth.urls')),
]


if settings.DEBUG:  # for development stage
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
