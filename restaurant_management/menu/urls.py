from django.urls import path
from .views import (
    MenuDishRetrieveUpdateDestroyView,
    ListActiveDishesByStatus,
    MenuDishCreateView
)
from .extra_views import list_dish_status

urlpatterns = [
    path('dishes/<int:id>/', 
         MenuDishRetrieveUpdateDestroyView.as_view(), 
         name='menu-item-detail'),
    
    path('dishes/by-status/', 
         ListActiveDishesByStatus.as_view(), 
         name='menu-dishes-by-status'),
    
    path('dishes/', 
         MenuDishCreateView.as_view(),
         name='menu-dishes-list-create'),

    path('dish-status/', list_dish_status, name='dish-status-list'),

]