from django.contrib import admin
from django.urls import path
from restaurant import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('v1/api/tables', views.create_table, name='create_table'),
    path('v1/api/tables/all', views.get_tables, name='get_tables'),
    path('v1/api/tables/<int:table_number>', views.get_table_by_number, name='get_table_by_number'),
    path('v1/api/tables/<int:table_number>/remove', views.delete_table_by_number, name='delete_table_by_number')

]
