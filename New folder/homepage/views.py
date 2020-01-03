from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from . models import Item


def home(request):
    context = {
        'item': Item.objects.all()
    }
    return render(request, 'homepage/home.html', context)


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'homepage/items_form.html'

    fields = ['title',
              # 'category',
              'price', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ItemListView(ListView):
    model = Item
    template_name = 'homepage/home.html'  # app/model_viewtype.html
    context_object_name = 'item'
    ordering = ['-date_posted']
    paginate_by = 6


# views for posts from  an individual user
class UserItemListView(ListView):
    model = Item
    template_name = 'homepage/user_item.html'  # app/model_viewtype.html
    context_object_name = 'user_item'
    paginate_by = 6

    def get_queryset(self):  # filtering based on username
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Item.objects.filter(author=user).order_by('-date_posted')


class ItemDetailView(DetailView):
    model = Item
    template_name = 'homepage/items_detail.html'


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    template_name = 'homepage/items_form.html'
    fields = ['title', 'content']

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
    template_name = 'homepage/items_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.author:
            return True
        return False


class SearchItemListView(ListView):
    model = Item
    template_name = 'homepage/search_results.html'  # app/model_viewtype.html
    context_object_name = 'search_item'
    paginate_by = 5

    def get_queryset(self):  # filtering based on username
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(
            Q(title__icontains=query)
        )
        return object_list.order_by('-date_posted')

    #object = get_object_or_404(Item, searchkey=self.kwargs.get('title'))
    # return Item.objects.filter(author=user).


def aboutus(request):
    return render(request, 'homepage/about.html', {'title': 'About'})
