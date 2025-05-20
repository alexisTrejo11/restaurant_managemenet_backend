from django.urls import path
from reservations.infrastructure.views.reservation_views import (
    get_reservations_by_date_range,
    today_list,
    schedule_reservation,
    update_reservation,
    cancel_reservation,
)

from orders.infrastructure.api.views.table_views import TableViews
from orders.infrastructure.api.views.order_admin_views import OrderViews
from menu.infrastructure.api.views.menu_views import MenuViews
from stock.infrastructure.api.views.stock_views import StockViews
from stock.infrastructure.api.views.ingredient_views import IngredientViews
from stock.infrastructure.api.views.stock_transaction_views import (
    register_stock_transaction,
    adjust_stock_transaction,
    delete_stock_transaction,
)
from authorization.views import (
    login,
    signup,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from rest_framework.routers import DefaultRouter



schema_view = get_schema_view(
   openapi.Info(
      title="Restaurant Management API",
      default_version='v1',
      description="Documentation for the API of a Restaurant Management System",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="aTrejoCoder@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'orders', OrderViews, basename='order') 
router.register(r'menus', MenuViews, basename='menu')
router.register(r'tables', TableViews, basename='table')
router.register(r'stocks', StockViews, basename='stock')
router.register(r'ingredients', IngredientViews, basename='ingredient')


urlpatterns = [
   path('', include(router.urls)),

   path('api/auth/signup/', signup, name='signup'),
   path('api/auth/login/', login, name='login'),

   path('api/reservations', get_reservations_by_date_range),
   path('api/reservations/today', today_list),
   path('api/reservations', schedule_reservation),
   path('api/reservations/<str:reservation_id>', update_reservation),
   path('api/reservations/cancel/<str:request_id>', cancel_reservation),

    path('api/stock/transactions', register_stock_transaction, name='register_stock_transaction'),
    path('api/stock/transactions/<str:transaction_id>', adjust_stock_transaction, name='adjust_stock_transaction'),
    path('api/stock/transactions/<str:transaction_id>/delete', delete_stock_transaction, name='delete_stock_transaction'),

    path('api/users/', include('users.urls')),

   # Swagger 
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-schema'),

]

"""
   path('api/auth/logout/', logout, name='logout'),
"""