from django.contrib import admin

from .models import NewsLetter, NewsletterUser


class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "date_added",
    )


admin.site.register(NewsletterUser, NewsletterAdmin)
admin.site.register(NewsLetter)
