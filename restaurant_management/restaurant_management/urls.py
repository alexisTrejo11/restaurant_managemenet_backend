from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant.views.ingredient_views import GetAllIngredients, GetIngredientById, CreateIngredient, DeleteIngredient
from restaurant.views.table_views import GetAllTables, GetTableByNumber, CreateTable, DeleteTable
from restaurant.views.menu_views import MenuViewSet
from restaurant.views.stock_views import StockViewSet
from restaurant.views.reservation_views import ReservationViews
from restaurant.views.order_views import OrderViews
from restaurant.views.payment_views import PaymentViews

menu_view_router = DefaultRouter()
menu_view_router.register(r'menus', MenuViewSet, basename='menu')

reservation_view_router = DefaultRouter()
reservation_view_router.register(r'reservations', ReservationViews, basename='reservation')

order_view_router = DefaultRouter()
order_view_router.register(r'orders', OrderViews, basename='orders')

payment_view_router = DefaultRouter()
payment_view_router.register(r'payments', PaymentViews, basename='payments')

urlpatterns = [
    # Tables
    path('v1/api/tables/<int:table_number>', GetTableByNumber.as_view(), name='get_table_by_number'),
    path('v1/api/tables/all', GetAllTables.as_view(), name='get_all_tables'),   
    path('v1/api/tables', CreateTable.as_view(), name='create_tables'),   
    path('v1/api/tables/<int:table_number>/delete', DeleteTable.as_view(), name='delete_tables_by_number'),   

    #Ingredients
    path('v1/api/ingredients/<int:ingredient_id>', GetIngredientById.as_view(), name='get_ingredient_by_id'),   
    path('v1/api/ingredients/all', GetAllIngredients.as_view(), name='get_all_ingredients'),   
    path('v1/api/ingredients', CreateIngredient.as_view(), name='delete_ingredient_by_id'),   
    path('v1/api/ingredients/<int:ingredient_id>/remove', DeleteIngredient.as_view(), name='delete_ingredient_by_id'),   

    # Menu view
    path('v1/api/', include(menu_view_router.urls)),

    # Stocks
    path('v1/api/stocks/', StockViewSet.as_view({'get': 'list', 'post': 'create'}), name='stock-list'),
    path('v1/api/stocks/<int:pk>/', StockViewSet.as_view({'get': 'get', 'delete': 'delete'}), name='stock-detail'),
    path('v1/api/stocks/ingredient/<int:ingredient_id>/', StockViewSet.as_view({'get': 'get_by_ingredient'}), name='stock-by-ingredient'),
    path('v1/api/stocks/transaction/', StockViewSet.as_view({'put': 'add_transaction'}), name='stock-by-ingredient'),

    # Resevations
    path('v1/api/reservations/<int:pk>/', ReservationViews.as_view({'get': 'getReservationById', 'delete': 'deleteById'}), name='stock-detail'),
    path('v1/api/reservations/today/', ReservationViews.as_view({'get': 'getTodayReservation'}), name='today-reservations'),
    path('v1/api/reservations/date-range/', ReservationViews.as_view({'get': 'getReservationByDateRange'}), name='reservations-dateRange'),
    path('v1/api/reservations/by', ReservationViews.as_view({'get': 'getReservationsByFilter'}), name='reservations-by-filter'),
    
    path('v1/api/reservations/', ReservationViews.as_view({'post': 'create'}), name='stock-list'),

    # Orders
    path('v1/api/orders/<int:id>/', OrderViews.as_view({'get': 'get_order_by_id', 'delete': 'delete_order'}), name='order-by-id'),
    path('v1/api/orders/by-status/<str:status>/', OrderViews.as_view({'get': 'get_orders_by_status'}), name='orders-by-status'),
    path('v1/api/orders/<int:table_number>', OrderViews.as_view({'post': 'start_order'}), name='start-order'),
    path('v1/api/orders/<int:id>/cancel', OrderViews.as_view({'put': 'cancel_order'}), name='cancel-order'),
    path('v1/api/orders/<int:id>/end', OrderViews.as_view({'put': 'end_order'}), name='complete-order'),


    path('v1/api/orders/<int:order_id>/<int:item_id>/deliver', OrderViews.as_view({'put': 'mark_item_as_delivered'}), name='mark_item_as_delivered'),
    path('v1/api/orders/items/add', OrderViews.as_view({'put': 'add_items_to_order'}), name='start-order'),
    path('v1/api/orders/items/remove', OrderViews.as_view({'delete': 'delete_items_to_order'}), name='start-order'),
    path('v1/api/orders/items/not-delivered', OrderViews.as_view({'get': 'get_not_delivered_items'}), name='get_not_delivered_items'),

    # Payment
    path('v1/api/payments/<int:id>', PaymentViews.as_view({'get': 'get_payment_by_id'}), name='get_payment_by_id'),
    path('v1/api/payments/by-status/<str:status>', PaymentViews.as_view({'get': 'get_payments_by_status'}), name='get_payment_by_id'),
    path('v1/api/payments/by-date/start/<str:start_date>/end/<str:end_date>', PaymentViews.as_view({'get': 'get_payments_by_data_range'}), name='get_payments_by_data_range'),
    path('v1/api/payments/by-date/today', PaymentViews.as_view({'get': 'get_today_payments'}), name='get_payments_by_data_range'),
    path('v1/api/payments/<int:id>/complete/<str:payment_method>', PaymentViews.as_view({'put': 'complete_payment'}), name='complete_payment'),
    path('v1/api/payments/<int:id>/cancel', PaymentViews.as_view({'put': 'cancel_payment'}), name='cancel_payment'),
] 
 
