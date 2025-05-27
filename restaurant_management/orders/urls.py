from django.urls import path, include
from .views.order_item_views import add_order_item, delete_order_item
from .views.order_views import OrderViewsSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', OrderViewsSet, basename='stock')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:order_id>/items/add/', add_order_item, name='order-add-items'),
    path('<int:order_id>/items/delete/', delete_order_item, name='order-delete-items'),
]