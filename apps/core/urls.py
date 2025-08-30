from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('exhibition/', views.exhibition, name='exhibition'),
    path('artfair/', views.artfair, name='artfair'),
    path('artists/', views.artists, name='artists'),
    path('frame/', views.frame, name='frame'),
    path('location/', views.location, name='location'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
]