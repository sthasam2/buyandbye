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
from . models import Item
# from . forms import ItemCreateForm


def home(request):
    context = {
        'item': Item.objects.all()
    }
    return render(request, 'homepage/home.html', context)


class ItemCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    # form_class = ItemCreateForm #to inherit from form
    model = Item
    template_name = 'homepage/items_form.html'
    fields = ['title', 'category', 'price', 'content', 'image', ]

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
