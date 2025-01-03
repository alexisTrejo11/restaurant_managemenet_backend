from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant.views.table_views import TableViews
from restaurant.views.menu_views import MenuViews
from restaurant.views.reservation_views import ReservationViews
from restaurant.views.order_views import OrderViews
from restaurant.views.stock_views import StockViews
from restaurant.views.payment_views import PaymentViews
from restaurant.views.ingredient_views import IngredientViews

urlpatterns = [
    # Tables
    path('v1/api/tables/<int:number>', TableViews.as_view({'get': 'get_table_by_number', 'delete': 'delete_table_by_number'}), name='table-detail'),
    path('v1/api/tables/all', TableViews.as_view({'get': 'get_all_tables'}), name='get_all_tables'),
    path('v1/api/tables', TableViews.as_view({'post': 'create_table'}), name='get_all_tables'),

    #Ingredients
    path('v1/api/ingredients/<int:ingredient_id>', IngredientViews.as_view({'get': 'get_ingredient_by_id', 'delete': 'delete_ingredient_by_id'}), name='ingredient-detail'),
    path('v1/api/ingredients/all', IngredientViews.as_view({'get': 'get_all_ingredients'}), name='get_all_ingredients'),
    path('v1/api/ingredients', IngredientViews.as_view({'post': 'create_ingredient'}), name='create_ingredient'),

    # Stocks
    path('v1/api/stocks/<int:stock_id>', StockViews.as_view({'get': 'get_stock_by_id', 'delete': 'delete_stock_by_id'}), name='stock-detail'),
    path('v1/api/stocks/ingredient/<int:ingredient_id>', StockViews.as_view({'get': 'get_stock_by_ingredient_id'}), name='get_stock_by_ingredient_id'),
    path('v1/api/stocks/all', StockViews.as_view({'get': 'get_all_stocks_sort_by_last_transaction'}), name='stock-detail'),
    path('v1/api/stocks', StockViews.as_view({'post': 'init_stock'}), name='init_stock'),
    path('v1/api/stocks/transaction', StockViews.as_view({'put': 'add_transaction'}), name='stock-by-ingredient'),

    # Menu view
    path('v1/api/menu_items/<int:menu_id>', MenuViews.as_view({'get': 'get_menu_item_by_id', 'delete': 'delete_menu_item_by_id'}), name='menu_item-detail'),
    path('v1/api/menu_items/all', MenuViews.as_view({'get': 'get_all_menu_items'}), name='get_all_menu_items'),
    path('v1/api/menu_items/category', MenuViews.as_view({'get': 'get_menus_items_by_category'}), name='get_menus_items_by_category'),
    path('v1/api/menu_items', MenuViews.as_view({'post': 'create_menu_item'}), name='create_menu_item'),

    # Resevations
    path('v1/api/reservations/<int:reservation_id>', ReservationViews.as_view({'get': 'get_reservation_by_id', 'delete': 'delete_reservation_by_id'}), name='reservation-detail'),
    path('v1/api/reservations/today', ReservationViews.as_view({'get': 'get_today_reservation'}), name='today-reservations'),
    path('v1/api/reservations/date-range', ReservationViews.as_view({'get': 'get_reservation_by_date_range'}), name='reservations-dateRange'),
    path('v1/api/reservations/by', ReservationViews.as_view({'get': 'get_reservations_by_filter'}), name='reservations-by-filter'),

    path('v1/api/reservations', ReservationViews.as_view({'post': 'create_reservation'}), name='create_reservation'),

    # Orders
    path('v1/api/orders/<int:id>', OrderViews.as_view({'get': 'get_order_by_id', 'delete': 'delete_order'}), name='order-by-id'),
    path('v1/api/orders/by-status/<str:status>', OrderViews.as_view({'get': 'get_orders_by_status'}), name='orders-by-status'),
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
 


