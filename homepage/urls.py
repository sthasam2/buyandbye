from django.urls import path
from . import views
from . views import (
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    UserItemListView,
)

urlpatterns = [
    # The homepage item view
    path('', ItemListView.as_view(), name='homepage'),
    # The individual user item view
    path('user/<str:username>', UserItemListView.as_view(), name='user-item'),
    # The individual item's detailed view
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),

    # The new item post creation view
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    # The existing item update view
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    # The existing item delete view
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),

    # The about page view
    path('about/', views.aboutus, name='aboutpage')
]
