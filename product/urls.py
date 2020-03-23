from django.urls import path
from hitcount.views import HitCountDetailView

from .views import category_views
from .views.category_views import CategoryListView, CategoryDetailView, load_subCat
from .views.item_views import(ItemCreateView, ItemDeleteView,
                              ItemDetailView, RecentItemListView, PopularItemListView, RecommendedItemListView, ItemUpdateView,
                              UserItemListView)
from .views.search_views import SearchItemListView, AdvancedSearchListView

# NOTE: only one views per url

urlpatterns = [
    # The product item view
    path('recent/', RecentItemListView.as_view(), name='recent-items'),
    path('popular/', PopularItemListView.as_view(), name='popular-items'),
    path('recommended/', RecommendedItemListView.as_view(),
         name='recommended-items'),
    # The individual user item view
    path('user/<str:username>', UserItemListView.as_view(), name='user-item'),
    # category page
    path('category/', CategoryListView.as_view(), name='category'),
    # The new item post creation view
    path('item/new', ItemCreateView.as_view(), name='item-create'),
    # The individual item's detailed view
    path('item/<slug:slug>', ItemDetailView.as_view(), name='item-detail'),

    path('category/<slug:slug>', CategoryDetailView.as_view(),
         name='category-detail'),
    # The existing item update view
    path('item/<slug:slug>/update', ItemUpdateView.as_view(), name='item-update'),
    # The existing item delete view
    path('item/<slug:slug>/delete', ItemDeleteView.as_view(), name='item-delete'),

    # The search results view
    path('search/', SearchItemListView.as_view(), name='search_results'),
    path('search/advanced', AdvancedSearchListView.as_view(),
         name='advanced_search_results'),

    path('ajax/load_subcategory/', category_views.load_subCat,
         name='ajax-load-subcategory'),
]
