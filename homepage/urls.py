from django.urls import path
from hitcount.views import HitCountDetailView

from .import views
from .views import (CategoryListView, ItemCreateView, ItemDeleteView,
                    ItemDetailView, ItemListView, ItemUpdateView,
                    SearchItemListView, UserItemListView)

# NOTE: only one views per url

urlpatterns = [
    # path('', views.base, name='base'),

    path('', views.home, name='homepage'),
    # The homepage item view
    path('item/latest/', ItemListView.as_view(), name='latest-item'),
    # The individual user item view
    path('user/<str:username>', UserItemListView.as_view(), name='user-item'),

        # The new item post creation view
    path('item/new', ItemCreateView.as_view(), name='item-create'),
    # The individual item's detailed view
    path('item/<slug:slug>', ItemDetailView.as_view(), name='item-detail'),


    # The existing item update view
    path('item/<slug:slug>/update', ItemUpdateView.as_view(), name='item-update'),
    # The existing item delete view
    path('item/<slug:slug>/delete', ItemDeleteView.as_view(), name='item-delete'),

    # The search results view
    path('search/', SearchItemListView.as_view(), name='search_results'),

    # The about page view
    path('about/', views.aboutus, name='about'),
    # The Privacy policy page
    path('privacy_policy/', views.privacy_policy, name='privacy-policy'),
    # terms and conditions
    path('terms_and_conditions/', views.terms_and_conditions, name='terms-and-conditions'),


    path('ajax/load_subcategory/', views.load_subCat, name='ajax-load-subcategory'),
]
