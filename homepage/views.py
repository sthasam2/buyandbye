from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy

from . models import Item, Category, SubCategory
# from . forms import ItemCreateForm

"""
    # pagination logic
    from django.core.paginator import Paginator

    def listing(request):
    contact_list = Contact.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.html', {'page_obj': page_obj})
"""

# def base(request):
#     frontend_stuff = {
#         'item': Item.objects.all(),
#         'category': Category.objects.all(),
#         # 'c_paginator' : Paginator('category', 20),
#         'sub_category': SubCategory.objects.all(),
#         # 's_paginator' : Paginator('sub_category', 20),
#     }
#     return render(request, 'homepage/base.html', frontend_stuff)

def home(request):
    frontend_stuff = {
        'item': Item.objects.all(),
        'category': Category.objects.all(),
        'c_paginator' : Paginator('category', 20),
        'sub_category': SubCategory.objects.all(),
        's_paginator' : Paginator('sub_category', 20),
    }
    return render(request, 'homepage/home.html', frontend_stuff)


class ItemCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    # form_class = ItemCreateForm #to inherit from form
    model = Item
    template_name = 'homepage/items_form.html'
    fields = ['title', 'category', 'sub_category',
              'price', 'condition', 'content', 'image', ]

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


class ItemListView(ListView):
    model = Item
    template_name = 'homepage/home.html'  # app/model_viewtype.html
    context_object_name = 'item'
    ordering = ['-date_posted']
    paginate_by = 8


# views for posts from  an individual user
class UserItemListView(ListView):
    model = Item
    template_name = 'homepage/user_item.html'  # app/model_viewtype.html
    context_object_name = 'user_item'
    paginate_by = 6

    def get_queryset(self):  # filtering based on username
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Item.objects.filter(author=user).order_by('-date_posted')


class CategoryListView(ListView):
    model = Category
    template_name = 'homepage/base.html'  # app/model_viewtype.html
    context_object_name = 'categorylist'
    ordering = ['name']


class ItemDetailView(DetailView):
    model = Item
    template_name = 'homepage/items_detail.html'


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    template_name = 'homepage/items_form.html'
    fields = ['title', 'category', 'sub_category', 'price', 'content', ]

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


def aboutus(request):
    return render(request, 'homepage/about.html', {'title': 'About'})


def privacy_policy(request):
    return render(request, 'homepage/privacypolicy.html', {'title': 'Privacy Policy'})
