from django.contrib import admin
from django.urls import path
from restaurant.views import table_views, ingredient_views, menu_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('v1/api/tables', table_views.create_table, name='create_table'),
    path('v1/api/tables/all', table_views.get_tables, name='get_tables'),
    path('v1/api/tables/<int:table_number>', table_views.get_table_by_number, name='get_table_by_number'),
    path('v1/api/tables/<int:table_number>/remove', table_views.delete_table_by_number, name='delete_table_by_number'),

    path('v1/api/ingredients', ingredient_views.create_ingredient, name='create_ingredients'),
    path('v1/api/ingredients/all', ingredient_views.get_ingredients, name='get_ingredients'),
    path('v1/api/ingredients/<int:ingredient_id>', ingredient_views.get_ingredient_by_id, name='get_ingredient_by_id'),
    path('v1/api/ingredients/<int:ingredient_id>/remove', ingredient_views.delete_ingredient_by_id, name='delete_ingredient_by_id'),

    path('v1/api/menus/category/<str:category>', menu_views.get_menus_by_category, name='get_menus_by_category'),
    path('v1/api/menus/<int:menu_id>', menu_views.get_menu_by_id, name='get_menu_by_id'),
    path('v1/api/menus', menu_views.create_menu, name='create_menu'),
    path('v1/api/menus/<int:menu_id>/remove', menu_views.delete_menu_by_id, name='delete_menu_by_id'),
]
