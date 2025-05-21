from django.urls import path
from .views import (
    MenuItemRetrieveUpdateDestroyView,
    ListActiveItemByStatus,
    MenuListCreateView
)

urlpatterns = [
    path('dishes/<int:id>/', 
         MenuItemRetrieveUpdateDestroyView.as_view(), 
         name='menu-item-detail'),
    
    path('dishes/by-status/', 
         ListActiveItemByStatus.as_view(), 
         name='menu-dishes-by-status'),
    
    path('dishes/', 
         MenuListCreateView.as_view(),
         name='menu-dishes-list-create'),
]