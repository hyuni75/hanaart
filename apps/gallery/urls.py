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
]