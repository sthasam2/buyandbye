from django.shortcuts import render
from homepage.models import Category, SubCategory, Item


def category_template(request):
    frontend_stuff = {
        'category': Category.objects.all(),
        'sub_category': SubCategory.objects.all(),
    }
    return frontend_stuff


def items_template(request):
    item_context = {
        'item': Item.objects.all().order_by('-date_posted')[:15],
        'popular_items': Item.objects.all().order_by('-hit_count_generic__hits')[:10],
    }
    return item_context
