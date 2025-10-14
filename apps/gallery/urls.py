# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('exhibition/', views.exhibition_list, name='exhibition_list'),      # 전시 목록
    path('exhibition/<int:pk>/', views.exhibition_detail, name='exhibition_detail'),  # 전시 상세
    path('artfair/', views.artfair_list, name='artfair_list'),              # 아트페어
    path('artist/', views.artist_list, name='artist_list'),                 # 작가
    path('frame/', views.frame, name='frame'),                              # 액자제작
]
