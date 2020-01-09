from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # homepage
    path('', include('homepage.urls')),

    # users
    path('', include('users.urls')),

    #markdownx requirement
    path('markdownx/', include('markdownx.urls')),
]


if settings.DEBUG:  # for development stage
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
