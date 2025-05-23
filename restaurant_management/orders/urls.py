from django.urls import path, include
from .views import OrderViewsSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', OrderViewsSet, basename='stock')

urlpatterns = [
    path('', include(router.urls)),
]