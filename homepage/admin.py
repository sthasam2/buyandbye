from django.contrib import admin

from .models import Category, Item, SubCategory


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'price', 'author', 'slug')
    list_filter = ('title', 'date_posted', 'price',)
    # prepopulated_fields ={"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug',)
    list_filter = ('name', 'slug',)
    prepopulated_fields = {"slug": ("name",)}

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('subname', 'parent_category', 'slug',)
    list_filter = ('subname',)
    # prepopulated_fields = {"slug": ("subname",)}


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
