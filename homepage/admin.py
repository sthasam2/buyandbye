from django.contrib import admin
from . models import Item, Category #, Sub_Category

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title',  'date_posted', 'price', 'author',)
    # prepopulated_fields ={'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # prepopulated_fields ={'slug': ('name',)}

admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Sub_Category)
