from django.urls import path
from . import views

app_name = 'navigator'

urlpatterns = [
    path('api/menu/', views.menu_api_list, name='menu_list'),
    path('api/menu/<int:pk>/', views.menu_api_detail, name='menu_detail'),
    path('api/menu/<int:pk>/toggle/', views.menu_toggle, name='menu_toggle'),
    path('api/menu/reorder/', views.menu_reorder, name='menu_reorder'),
]