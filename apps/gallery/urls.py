from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    # 공개 페이지 (Public Views)
    path('artists/', views.artist_list, name='artist_list'),
    path('artists/<int:pk>/', views.artist_detail, name='artist_detail'),
    path('exhibitions/', views.exhibition_list, name='exhibition_list'),
    path('exhibitions/<slug:slug>/', views.exhibition_detail, name='exhibition_detail'),
    path('artworks/<int:pk>/', views.artwork_detail, name='artwork_detail'),
    path('location/', views.location, name='location'),
    path('frame/', views.frame, name='frame'),
    
    # 관리 페이지 (Manage Views) - /manage/ prefix로 접근
    # Artists Management
    path('manage/artists/', views.artist_manage_list, name='artist_manage_list'),
    path('manage/artists/create/', views.artist_create, name='artist_create'),
    path('manage/artists/<int:pk>/edit/', views.artist_edit, name='artist_edit'),
    path('manage/artists/<int:pk>/delete/', views.artist_delete, name='artist_delete'),
    
    # Exhibitions Management
    path('manage/exhibitions/', views.exhibition_manage_list, name='exhibition_manage_list'),
    path('manage/exhibitions/create/', views.exhibition_create, name='exhibition_create'),
    path('manage/exhibitions/<int:pk>/edit/', views.exhibition_edit, name='exhibition_edit'),
    path('manage/exhibitions/<int:pk>/delete/', views.exhibition_delete, name='exhibition_delete'),
    path('manage/exhibitions/<int:pk>/set-current/', views.exhibition_set_current, name='exhibition_set_current'),
    
    # Artworks Management
    path('manage/artworks/', views.artwork_manage_list, name='artwork_manage_list'),
    path('manage/artworks/create/', views.artwork_create, name='artwork_create'),
    path('manage/artworks/<int:pk>/edit/', views.artwork_edit, name='artwork_edit'),
    path('manage/artworks/<int:pk>/delete/', views.artwork_delete, name='artwork_delete'),
    
    # 로그인/로그아웃
    path('manage/login/', views.manage_login, name='manage_login'),
    path('manage/logout/', views.manage_logout, name='manage_logout'),
    
    # Admin Dashboard (Root manage path)
    path('manage/', views.admin_dashboard, name='admin_dashboard'),
    path('manage/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]