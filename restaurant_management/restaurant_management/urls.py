from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant.views import table_views

urlpatterns = [
    path('v1/api/tables/<int:table_number>', table_views.get_table_by_number, name='get_table_by_number'),
    path('v1/api/tables/all', table_views.get_all_tables, name='get_all_tables'),   
    path('v1/api/tables', table_views.create_table, name='create_tables'),   
    path('v1/api/tables/<int:table_number>/delete', table_views.delete_table_by_number, name='delete_tables_by_number'),   

]
