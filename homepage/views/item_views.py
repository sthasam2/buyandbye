""" ITEM VIEWS """

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
# from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)
# local
from hitcount.views import HitCountDetailView
from homepage.forms import ItemCreateForm
from homepage.models import Item


# PRODUCT CRUD
""" CREATE"""


class ItemCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """ Product Item Creation using Django View: CreateView"""
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


""" / CREATE """

""" READ """


class RecentItemListView(ListView):
    """ Recent Product List using Django View: ListView"""
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
    """ Popular Product List using Django View: ListView """
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



class UserItemListView(ListView):
    """ Particular User's Posted Product List using Django View: ListView """
    model = Item
    template_name = 'homepage/items/user_item.html'  # app/model_viewtype.html
    context_object_name = 'user_item'
    paginate_by = 6

    def get_queryset(self):  # filtering based on username
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Item.objects.filter(author=user).order_by('-date_posted')


class ItemDetailView(HitCountDetailView):
    """ Individual Product Deatil using Django View: DetailView """
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


""" / READ """

""" UPDATE """


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Individual Product Update using Django View: UpdateView """
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


""" / UPDATE """

""" DELETE """


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Individual Product Delete using Django View: DeleteView """
    model = Item
    template_name = 'homepage/items/items_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.author:
            return True
        return False


""" / DELETE """