from django.shortcuts import render
from homepage.models import Category, SubCategory


def category(request):
    frontend_stuff = {
        'category': Category.objects.all(),
        'sub_category': SubCategory.objects.all(),
    }
    return frontend_stuff
