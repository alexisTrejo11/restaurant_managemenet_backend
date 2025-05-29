from django.urls import path, include
from .views.dish_views import (
    DishViewSet
)
from .views.dish_extra_views import list_dish_status, ListActiveDishesByStatus
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', DishViewSet, basename='menu')

urlpatterns = [
    path('', include(router.urls)),

    path('dish-status/', list_dish_status, name='dish-status-list'),
]