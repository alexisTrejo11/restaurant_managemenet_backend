from django.contrib import admin
from django.urls import path
from restaurant.views import table_views, ingredient_views, menu_views, reservation_views, stock_views, order_views, payment_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Table Endpoints
    path('v1/api/tables/all', table_views.get_tables, name='get_tables'),
    path('v1/api/tables/<int:table_number>', table_views.get_table_by_number, name='get_table_by_number'),
    
    path('v1/api/tables', table_views.create_table, name='create_table'),
    path('v1/api/tables/<int:table_number>/remove', table_views.delete_table_by_number, name='delete_table_by_number'),

    # Ingredient Endpoints
    path('v1/api/ingredients/all', ingredient_views.get_all_ingredients, name='get_all_ingredients'),
    path('v1/api/ingredients/<int:ingredient_id>', ingredient_views.get_ingredient_by_id, name='get_ingredient_by_id'),

    path('v1/api/ingredients', ingredient_views.create_ingredient, name='create_ingredients'),
    path('v1/api/ingredients/<int:ingredient_id>/remove', ingredient_views.delete_ingredient_by_id, name='delete_ingredient_by_id'),

    # Menu Endpoints
    path('v1/api/menus/category/<str:category>', menu_views.get_menus_by_category, name='get_menus_by_category'),
    path('v1/api/menus/<int:menu_id>', menu_views.get_menu_by_id, name='get_menu_by_id'),

    path('v1/api/menus', menu_views.create_menu, name='create_menu'),
    path('v1/api/menus/<int:menu_id>/remove', menu_views.delete_menu_by_id, name='delete_menu_by_id'),

    # Reservation Endpoints
    path('v1/api/reservations/<int:reservation_id>', reservation_views.get_reservation_by_id, name='get_reservation_by_id'),
    path('v1/api/reservations/email/<str:email>', reservation_views.get_reservations_by_email, name='get_reservation_by_email'),
    path('v1/api/reservations/today', reservation_views.get_today_reservations, name='get_today_reservations'),
    path('v1/api/reservations/today/not-expired', reservation_views.get_today_not_expired_reservations, name='get_today_not_expired_reservations'),
    path('v1/api/reservations/start/<str:start_date>/end/<str:end_date>', reservation_views.get_reservations_by_date_range, name='get_reservations_by_date_range'),

    path('v1/api/reservations', reservation_views.create_reservation, name='create_reservation'),
    path('v1/api/reservations/<int:reservation_id>/remove', reservation_views.delete_reservation_by_id, name='delete_reservation_by_id'),

    # Stock Endpoints
    path('v1/api/stock/<int:stock_id>', stock_views.get_stock_by_id, name='get_stock_by_id'),
    path('v1/api/stock/ingredient/<int:ingredient_id>', stock_views.get_stock_by_ingredient_id, name='get_stock_by_id'),
    
    path('v1/api/stock/ingredient/<int:ingredient_id>/init', stock_views.init_stock, name='init_stock_by_ingredient_id'),
    path('v1/api/stock/update', stock_views.update_stock_by_ingredient_id, name='update_stock_by_ingredient_id'),
    path('v1/api/stock/ingredient/<int:ingredient_id>/remove', stock_views.delete_stock_by_ingredient_id, name='deldelete_stock_by_ingredient_id'),

    # Order Endpoints 
    path('v1/api/orders/<int:order_id>', order_views.get_order_by_id, name='get_order_by_id'),
    path('v1/api/orders/status/<str:order_status>', order_views.get_orders_by_status, name='get_orders_by_status'),
    path('v1/api/orders/init', order_views.init_order, name='init_order'),
    path('v1/api/orders/<int:order_id>/add-items', order_views.add_items_to_order, name='add_items_to_order'),
    path('v1/api/orders/<int:order_id>/finish', order_views.finish_order, name='finish_order'),
    path('v1/api/orders/<int:order_id>/cancel', order_views.cancel_order, name='cancel_order'),

    # Payment Endpoints
    path('v1/api/payments/<int:payment_id>', payment_views.get_payment_by_id, name='get_order_by_id'),
    path('v1/api/payments/status/<str:payment_status>', payment_views.get_payments_by_status, name='get_payments_by_status'),
    path('v1/api/payments/by-date/start/<str:start_date>/end/<str:end_date>', payment_views.get_payments_by_data_range, name='get_payments_by_data_range'),
    path('v1/api/payments/today', payment_views.get_today_payments, name='get_today_payments'),
    path('v1/api/payments/<int:payment_id>/complete', payment_views.complete_payment, name='complete_payment'),
    path('v1/api/payments/<int:payment_id>/cancel', payment_views.cancel_payment, name='complete_payment'),

]
