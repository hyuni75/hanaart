# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),              # 홈
    path('about/', views.about, name='about'),      # 인사말
    path('history/', views.history, name='history'),  # 연혁
    path('contact/', views.contact, name='contact'),  # 연락처
]
