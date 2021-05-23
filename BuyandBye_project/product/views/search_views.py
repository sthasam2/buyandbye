""" VIEWS for product """

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from product.models import Item
# from product.forms import AdvancedSearchForm


def is_valid_queryparam(param):
    """Function to check whether the input parameters are valid of not"""
    return param != '' and param is not None


"""------------------------------------------------------READ------------------------------------------------------"""


class SearchItemListView(ListView):
    """ List view for listing search item"""
    paginate_by = 10
    model = Item
    template_name = 'product/search/search_results.html'  # app/model_viewtype.html
    context_object_name = 'search_item'

    def get_queryset(self):  # queryset using Q object
        query = self.request.GET.get('q')
        object_list = Item.objects.all()
        """Filter based on Query"""
        if is_valid_queryparam(query):
            object_list = object_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(author__username__icontains=query)
            ).distinct()
        else:
            object_list = object_list.none()

        return object_list.order_by('-date_posted')


class AdvancedSearchListView(ListView):
    """List view for advanced filtering"""
    # form = AdvancedSearchForm
    # model = Item
    paginate_by = 10
    template_name = 'product/search/advanced_search_results.html'
    context_object_name = 'advanced_search_item'

    def get_queryset(self):
        # print("adv")
        object_list = Item.objects.all()

        title_asq = self.request.GET.get('title_as')
        print(title_asq)
        price_low_asq = self.request.GET.get('price_low_as')
        price_high_asq = self.request.GET.get('price_high_as')
        category_asq = self.request.GET.get('category_as')
        date_posted_asq = self.request.GET.get('date_posted_as')
        invalid = 0

        if is_valid_queryparam(title_asq):
            object_list = object_list.filter(
                Q(title__icontains=title_asq))
            invalid = invalid + 1

        if is_valid_queryparam(price_high_asq):
            object_list = object_list.filter(
                Q(price__lte=float(price_high_asq)))
            invalid = invalid + 1

        if is_valid_queryparam(price_low_asq):
            object_list = object_list.filter(
                Q(price__gte=float(price_low_asq)))
            invalid = invalid + 1

        if is_valid_queryparam(category_asq):
            object_list = object_list.filter(
                Q(category=category_asq))
            invalid = invalid + 1

        if is_valid_queryparam(date_posted_asq):
            object_list = object_list.filter(
                Q(date_posted__gte=date_posted_asq))
            invalid = invalid + 1

        print(invalid)

        if invalid == 0:
            object_list = object_list.none()

        return object_list.order_by('-date_posted')