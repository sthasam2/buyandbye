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
# from django.utils.text import slugify
# local
from hitcount.views import HitCountDetailView

from .forms import ItemCreateForm
from .models import Category, Item, SubCategory

# from .forms import ItemCreateForm

"""
    # pagination logic
    item = Item.objects.all().order_by('-date_posted')[:10]
    category = Category.objects.all(),
    sub_category = SubCategory.objects.all(),
    popular_items = Item.objects.all().order_by(
        '-hit_count_generic__hits')[:10],

    paginator = Paginator(item, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    frontend_stuff = {
        'item': item,
        'category': category,
        'sub_category': sub_category,
        'popular_items': popular_items,
        # 'page_obj': page_obj
    }
"""


def home(request):
    frontend_stuff = {
        'item': Item.objects.all().order_by('-date_posted')[:15],
        'popular_items': Item.objects.all().order_by('-hit_count_generic__hits')[:10],
    }
    return render(request, 'homepage/home.html', frontend_stuff)


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

    # def image_upload(request):
    #     context={}
    #     if request.method == 'POST':
    #         image= request.FILES('image')
    #         fs = FileSystemStorage()
    #         name = fs.save(image.name, image)
    #         context['url'] = fs.url(name)
    #     return render(request, 'item-detail', context)

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class()
    #     return render(request, self.template_name, {'form': form})
    #
    # def upload_file(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         item_create_form = self.form_class(request.POST, request.FILES)
    #         if item_create_form.is_valid():
    #             instance = Item(file_field=request.FILES['file'])
    #             instance.save()
    #             messages.success(request, f'Item added successfully')
    #             return redirect('item/<int:pk>')
    #     else:
    #         return render(request, self.template_name, {'form': item_create_form})

# Item CRUD


class ItemListView(ListView):
    model = Item
    template_name = 'homepage/home.html'  # app/model_viewtype.html
    context_object_name = 'item'
    ordering = ['-date_posted']
    paginate_by = 8


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
    template_name = 'homepage/base.html'  # app/model_viewtype.html
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
