from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('artists/', views.artist_list, name='artist_list'),
    path('artists/<int:pk>/', views.artist_detail, name='artist_detail'),
    path('exhibitions/', views.exhibition_list, name='exhibition_list'),
    path('exhibitions/<slug:slug>/', views.exhibition_detail, name='exhibition_detail'),
    path('artworks/<int:pk>/', views.artwork_detail, name='artwork_detail'),
    path('location/', views.location, name='location'),
    path('frame/', views.frame, name='frame'),
    
    # CRUD URLs for Artists
    path('admin/artists/', views.artist_manage_list, name='artist_manage_list'),
    path('admin/artists/create/', views.artist_create, name='artist_create'),
    path('admin/artists/<int:pk>/edit/', views.artist_edit, name='artist_edit'),
    path('admin/artists/<int:pk>/delete/', views.artist_delete, name='artist_delete'),
    
    # CRUD URLs for Exhibitions
    path('admin/exhibitions/', views.exhibition_manage_list, name='exhibition_manage_list'),
    path('admin/exhibitions/create/', views.exhibition_create, name='exhibition_create'),
    path('admin/exhibitions/<int:pk>/edit/', views.exhibition_edit, name='exhibition_edit'),
    path('admin/exhibitions/<int:pk>/delete/', views.exhibition_delete, name='exhibition_delete'),
    path('admin/exhibitions/<int:pk>/set-current/', views.exhibition_set_current, name='exhibition_set_current'),
    
    # CRUD URLs for Artworks
    path('admin/artworks/', views.artwork_manage_list, name='artwork_manage_list'),
    path('admin/artworks/create/', views.artwork_create, name='artwork_create'),
    path('admin/artworks/<int:pk>/edit/', views.artwork_edit, name='artwork_edit'),
    path('admin/artworks/<int:pk>/delete/', views.artwork_delete, name='artwork_delete'),
    
    # Admin Dashboard
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]