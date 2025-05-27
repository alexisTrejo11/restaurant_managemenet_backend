from django.urls import path
from authorization.views import login,signup
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tables.views import TableViews

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
router.register(r'tables', TableViews, basename='table')

urlpatterns = [
   path('api/', include(router.urls)),

   path('api/auth/signup/', signup, name='signup'),
   path('api/auth/login/', login, name='login'),
   path('api/users/', include('users.urls')),
   path('api/menu/',  include('menu.urls')),
   path('api/stock/',  include('stock.urls')),
   path('api/orders/',  include('orders.urls')),
   path('api/reservations/',  include('reservations.urls')),
   path('api/payments/',  include('payments.urls')),

   # Swagger 
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-schema'),

]
