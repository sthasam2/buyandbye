""" VIEWS for product """

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (DetailView, ListView)
from django.db.models import Q
# local
from product.models import Category, SubCategory, Item
from activity.utils import create_action


""" CATEGORY READ (R) """


class CategoryListView(ListView):
    """ Category List using Django View: ListView """
    model = Category
    template_name = 'product/category/category_page.html'  # app/model_viewtype.html
    context_object_name = 'categorylist'
    ordering = ['name']


class CategoryDetailView(DetailView):
    """ Category Detail using Django View: DetailView """
    model = Category
    template_name = 'product/category/category_detail.html'
    context_object_name = 'category_item'

    def create_activity(self):
        category_id = self.object
        create_action(self.request.user, 'Browsed category', category_id)

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        cat_name = self.object.name
        if self.request.user:
            self.create_activity()
        context.update({
            'cat_item': Item.objects.filter(Q(category__name=cat_name))
        })
        return context


def load_subCat(request):
    """ Funcion for loading subcategories based on parent_category """
    category_id = request.GET.get('category')
    sub_categories = SubCategory.objects.filter(
        parent_category_id=category_id).order_by('subname')
    context = {
        'sub_categories': sub_categories
    }
    return render(request, 'product/category/subCat_dropdown_list_options.html', context)
