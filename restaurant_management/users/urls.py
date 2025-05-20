from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListAPIView.as_view(), name='user-list'),
    path('create/', views.UserCreateAPIView.as_view(), name='user-create'),
    path('<int:pk>/', views.UserRetrieveAPIView.as_view(), name='user-detail'),
    path('<int:pk>/update/', views.UserUpdateAPIView.as_view(), name='user-update'),
    path('<int:pk>/delete/', views.UserDestroyAPIView.as_view(), name='user-delete'),
    
    #path('search/', views.UserSearchView.as_view(), name='user-search'),
]