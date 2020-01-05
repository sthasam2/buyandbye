from django.contrib import admin
from . models import Item, Category #, SubCategory

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'price', 'author',)
    list_filter = ('title', 'date_posted', 'price',)
    prepopulated_fields ={"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {"slug": ("name",)}

# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ('subname',)
#     list_filter = ('subname',)
#     prepopulated_fields = {"slug": ("subname",)}


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(SubCategory, SubCategoryAdmin)
