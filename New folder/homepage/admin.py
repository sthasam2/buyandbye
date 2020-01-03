from django.contrib import admin
from . models import Item, Category #, Sub_Category

admin.site.register(Item)
admin.site.register(Category)
# admin.site.register(Sub_Category)
