from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant.views.ingredient_views import GetAllIngredients, GetIngredientById, CreateIngredient, DeleteIngredient
from restaurant.views.table_views import GetAllTables, GetTableByNumber, CreateTable, DeleteTable
from restaurant.views.menu_views import MenuViewSet

router = DefaultRouter()
router.register(r'menus', MenuViewSet, basename='menu')

urlpatterns = [
    path('v1/api/tables/<int:table_number>', GetTableByNumber.as_view(), name='get_table_by_number'),
    path('v1/api/tables/all', GetAllTables.as_view(), name='get_all_tables'),   
    path('v1/api/tables', CreateTable.as_view(), name='create_tables'),   
    path('v1/api/tables/<int:table_number>/delete', DeleteTable.as_view(), name='delete_tables_by_number'),   


    path('v1/api/ingredients/<int:ingredient_id>', GetIngredientById.as_view(), name='get_ingredient_by_id'),   
    path('v1/api/ingredients/all', GetAllIngredients.as_view(), name='get_all_ingredients'),   
    path('v1/api/ingredients', CreateIngredient.as_view(), name='delete_ingredient_by_id'),   
    path('v1/api/ingredients/<int:ingredient_id>/remove', DeleteIngredient.as_view(), name='delete_ingredient_by_id'),   

    path('v1/api/', include(router.urls)),
]
