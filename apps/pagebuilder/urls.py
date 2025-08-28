from django.urls import path
from . import views

app_name = 'pagebuilder'

urlpatterns = [
    path('', views.PageListView.as_view(), name='page_list'),
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
    path('<int:page_id>/like/', views.toggle_like, name='toggle_like'),
    path('<int:page_id>/comment/', views.add_comment, name='add_comment'),
]