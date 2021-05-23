""" ITEM VIEWS """

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

# local
from hitcount.views import HitCountDetailView
from product.forms import ItemCreateForm
from product.models import Item
from recommender.utils import recommend, user_recommend
from activity.utils import create_action


"""------------------------------------------------------CREATE------------------------------------------------------"""


class ItemCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """ Product Item Creation using Django View: CreateView"""

    model = Item
    form_class = ItemCreateForm
    template_name = "product/items/items_form.html"
    # fields = ['title', 'category', 'sub_category',
    #           'price', 'condition', 'content', 'image', ]
    success_message = f"Item was succesfully created."
    # success_url = reverse_lazy('item-detail') #success url not required for CreateView and UpdateView

    def create_activity(self):
        print("item history created")
        activity = create_action(self.object.author, "Posted item", self.object)
        return activity

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        self.create_activity()
        return super(ItemCreateView, self).form_valid(form)

    # def save(self):
    #     super().save()
    #     self.create_activity()


"""------------------------------------------------------READ------------------------------------------------------"""


class RecentItemListView(ListView):
    """ Recent Product List using Django View: ListView"""

    model = Item
    template_name = "product/list_view/item_list.html"  # app/model_viewtype.html
    context_object_name = "item"
    ordering = ["-date_posted"]
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(RecentItemListView, self).get_context_data(**kwargs)
        context.update({"title": "Recent Items"})
        return context


class PopularItemListView(ListView):
    """ Popular Product List using Django View: ListView """

    model = Item
    template_name = "product/list_view/item_list.html"  # app/model_viewtype.html
    context_object_name = "item"
    ordering = ["-hit_count_generic__hits"]
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(PopularItemListView, self).get_context_data(**kwargs)
        context.update({"title": "Popular Items"})
        return context


class RecommendedItemListView(ListView):
    """ Popular Product List using Django View: ListView """

    model = Item
    template_name = "product/list_view/item_list.html"  # app/model_viewtype.html
    context_object_name = "item"
    ordering = ["-date_posted"]

    def get_context_data(self, **kwargs):
        context = super(RecommendedItemListView, self).get_context_data(**kwargs)
        user = self.request.user

        try:
            # if user.id is not None:
            rec_item = user_recommend(user)
        except:
            try:
                rec_item = user_recommend(1)
            except:
                rec_item = []

        context.update(
            {
                "title": "Recommended Items",
                "item": Item.objects.filter(id__in=rec_item),
            }
        )
        return context


class UserItemListView(ListView):
    """ Particular User's Posted Product List using Django View: ListView """

    model = Item
    template_name = "product/items/user_item.html"  # app/model_viewtype.html
    context_object_name = "user_items"
    paginate_by = 10

    def get_queryset(self):  # filtering based on username
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Item.objects.filter(author=user).order_by("-date_posted")

    def get_context_data(self, **kwargs):
        context = super(UserItemListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get("username"))

        context.update(
            {
                "title": f"Items by {user}",
                "user": user,
                "user_items": Item.objects.filter(author=user).order_by("-date_posted"),
            }
        )
        return context


class ItemDetailView(HitCountDetailView):
    """ Individual Product Deatil using Django View: DetailView """

    model = Item
    template_name = "product/items/items_detail.html"
    # hit count when set to true
    context_object_name = "item_detail"
    count_hit = True

    def create_activity(self):
        item_id = self.object
        # print(item_id.title)
        if self.request.user:
            create_action(self.request.user, "Viewed item", item_id)

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)

        if self.request.user.id is not None:
            self.create_activity()

        reco_item_id = recommend(self.object.id, 5)

        context.update(
            {
                "popular_items": Item.objects.order_by("-hit_count_generic__hits")[:5],
                "recommended_items": Item.objects.filter(id__in=reco_item_id),
            }
        )
        return context


"""------------------------------------------------------UPDATE------------------------------------------------------"""


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Individual Product Update using Django View: UpdateView """

    model = Item
    form_class = ItemCreateForm
    template_name = "product/items/items_form.html"
    # fields = ['title', 'category', 'sub_category',
    #           'price', 'condition', 'content', 'image', ]

    def create_activity(self):
        item_id = self.object
        activity = create_action(self.object.author, "Updated item", item_id)
        return activity

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        self.create_activity()
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


"""------------------------------------------------------DELETE------------------------------------------------------"""


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Individual Product Delete using Django View: DeleteView """

    model = Item
    template_name = "product/items/items_confirm_delete.html"
    success_url = "/"

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.author:
            return True
        return False

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        # history creation
        item_id = self.object
        create_action(self.request.user, "Deleted item", item_id)
        print("item deleted")
        return super(ItemDeleteView, self).delete(*args, **kwargs)