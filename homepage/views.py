""" VIEWS for product """

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)
# local
from hitcount.views import HitCountDetailView

from .forms import ItemCreateForm
from .models import Category, Item, SubCategory


def home(request):
    return render(request, 'homepage/home.html')


class ItemCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """ Django's create view for creating Item"""
    model = Item
    form_class = ItemCreateForm
    template_name = 'homepage/items/items_form.html'
    # fields = ['title', 'category', 'sub_category',
    #           'price', 'condition', 'content', 'image', ]

    success_message = f'Item was succesfully created.'
    # success_url = reverse_lazy('item-detail') #success url not required for CreateView and UpdateView

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecentItemListView(ListView):
    model = Item
    template_name = 'homepage/list_view/item_list.html'  # app/model_viewtype.html
    context_object_name = 'item'
    ordering = ['-date_posted']
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(RecentItemListView, self).get_context_data(**kwargs)
        context.update({
            'title': 'Recent Items'
        })
        return context


class PopularItemListView(ListView):
    model = Item
    template_name = 'homepage/list_view/item_list.html'  # app/model_viewtype.html
    context_object_name = 'item'
    ordering = ['-hit_count_generic__hits']
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(PopularItemListView, self).get_context_data(**kwargs)
        context.update({
            'title': 'Popular Items'
        })
        return context


class ItemDetailView(HitCountDetailView):
    model = Item
    template_name = 'homepage/items/items_detail.html'
    # hit count when set to true
    context_object_name = 'item_detail'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context.update({
            'popular_items': Item.objects.order_by('-hit_count_generic__hits')[:5],
        })
        return context


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = ItemCreateForm
    template_name = 'homepage/items/items_form.html'
    # fields = ['title', 'category', 'sub_category',
    #           'price', 'condition', 'content', 'image', ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'homepage/items/items_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.author:
            return True
        return False

# / Item CRUD


# views for posts from  an individual user
class UserItemListView(ListView):
    model = Item
    template_name = 'homepage/items/user_item.html'  # app/model_viewtype.html
    context_object_name = 'user_item'
    paginate_by = 6

    def get_queryset(self):  # filtering based on username
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Item.objects.filter(author=user).order_by('-date_posted')


# CATEGORY R
class CategoryListView(ListView):
    """ Listing for Category """
    model = Category
    template_name = 'homepage/category/category_page.html'  # app/model_viewtype.html
    context_object_name = 'categorylist'
    ordering = ['name']


class SearchItemListView(ListView):
    """ LIst view for listing search item"""
    model = Item
    template_name = 'homepage/search/search_results.html'  # app/model_viewtype.html
    context_object_name = 'search_item'
    paginate_by = 5

    def get_queryset(self):  # queryset using Q object
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()
        return object_list.order_by('-date_posted')


def load_subCat(request):
    """views for loading subcategory depending on the category in itemcreate form"""
    category_id = request.GET.get('category')
    sub_categories = SubCategory.objects.filter(
        parent_category_id=category_id).order_by('subname')
    return render(request, 'homepage/category/subCat_dropdown_list_options.html', {
        'sub_categories': sub_categories
    })


def aboutus(request):
    """ About page """
    return render(request, 'homepage/about.html', {'title': 'About'})


def privacy_policy(request):
    """ PRIVACY POLICY page """
    return render(request, 'homepage/privacypolicy.html', {'title': 'Privacy Policy'})


def terms_and_conditions(request):
    """ TERMS AND CONDITION page """
    return render(request, 'homepage/terms_conditions.html', {'title': 'Terms and Conditions'})
