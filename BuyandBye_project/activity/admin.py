from django.contrib import admin

from .models import Activity


class ActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "verb", "target", "date_created")
    list_filter = ("date_created",)
    search_fields = ("verb",)


admin.site.register(Activity, ActivityAdmin)
