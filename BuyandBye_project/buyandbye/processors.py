from django.shortcuts import render
from product.models import Category, SubCategory, Item
from recommender.utils import user_recommend


def category_template(request):
    frontend_stuff = {
        'category': Category.objects.all(),
        'sub_category': SubCategory.objects.all(),
    }
    return frontend_stuff


def items_template(request):
    user = request.user
    if user.id is not None:
        urec_item = user_recommend(user)
    else:
        urec_item = user_recommend(1)
    item_context = {
        'item': Item.objects.all().order_by('-date_posted')[:15],
        'popular_items': Item.objects.all().order_by('-hit_count_generic__hits')[:10],
        'rec_item': Item.objects.filter(id__in=urec_item)[:10]
    }
    return item_context
