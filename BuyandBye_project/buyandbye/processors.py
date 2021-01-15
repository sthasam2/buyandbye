from django.shortcuts import render
from product.models import Category, SubCategory, Item
from recommender.utils import user_recommend


def category_template(request):
    try:
        frontend_stuff = {
            'category': Category.objects.all(),
            'sub_category': SubCategory.objects.all(),
        }
        return frontend_stuff
    except:
        return {
            'category': None,
            'sub_category': None,
        }

def items_template(request):
    user = request.user
    try:
        if user.id is not None:
            urec_item = user_recommend(user)
        else:
            urec_item = user_recommend(1)
        item_context = {
            'items': Item.objects.all().order_by('-date_posted')[:15],
            'popular_items': Item.objects.all().order_by('-hit_count_generic__hits')[:10],
            'rec_items': Item.objects.filter(id__in=urec_item)[:10]
        }
        return item_context
    except:
        return {
            'items': None,
            'popular_items': None,
            'rec_items': None
        }
