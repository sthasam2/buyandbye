from django.urls import path
from .import views
from .views import (
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    UserItemListView,
)

urlpatterns = [
    path('', ItemListView.as_view(), name='homepage'),
    path('user/<str:username>', UserItemListView.as_view(), name='user-item'),

    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),

    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),

    path('about/', views.aboutus, name='aboutpage')
]
