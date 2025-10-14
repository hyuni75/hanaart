# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # 인증
    path('login/', views.login_view, name='login'),                    # 로그인
    path('logout/', views.logout_view, name='logout'),                 # 로그아웃

    # 관리 페이지
    path('', views.index, name='index'),                              # 관리자 메인
    path('home-design/', views.home_design_manage, name='home_design_manage'),  # 홈 디자인 관리
    path('template/', views.template_manage, name='template_manage'),  # 템플릿 섹션 관리
    path('artist/', views.artist_manage, name='artist_manage'),        # 작가 관리
    path('artwork/', views.artwork_manage, name='artwork_manage'),     # 작품 관리
    path('exhibition/', views.exhibition_manage, name='exhibition_manage'),  # 전시 관리
    path('artfair/', views.artfair_manage, name='artfair_manage'),     # 아트페어 관리
    path('history/', views.history_manage, name='history_manage'),     # 연혁 관리
    path('about/', views.about_manage, name='about_manage'),           # 인사말 관리
    path('frame/', views.frame_manage, name='frame_manage'),           # 액자 관리
    path('contact/', views.contact_manage, name='contact_manage'),     # 연락처 관리

    # API
    path('api/statistics/', views.statistics_api, name='statistics_api'),  # 통계 API

    # 연혁 API
    path('api/history/list/', views.history_list_api, name='history_list_api'),
    path('api/history/<int:pk>/', views.history_detail_api, name='history_detail_api'),
    path('api/history/create/', views.history_create_api, name='history_create_api'),
    path('api/history/<int:pk>/', views.history_update_api, name='history_update_api'),
    path('api/history/<int:pk>/', views.history_delete_api, name='history_delete_api'),

    # 아트페어 API
    path('api/artfair/list/', views.artfair_list_api, name='artfair_list_api'),
    path('api/artfair/<int:pk>/', views.artfair_detail_api, name='artfair_detail_api'),
    path('api/artfair/create/', views.artfair_create_api, name='artfair_create_api'),
    path('api/artfair/<int:pk>/update/', views.artfair_update_api, name='artfair_update_api'),
    path('api/artfair/<int:pk>/delete/', views.artfair_delete_api, name='artfair_delete_api'),

    # 작가 API
    path('api/artist/list/', views.artist_list_api, name='artist_list_api'),
    path('api/artist/<int:pk>/', views.artist_detail_api, name='artist_detail_api'),
    path('api/artist/create/', views.artist_create_api, name='artist_create_api'),
    path('api/artist/<int:pk>/update/', views.artist_update_api, name='artist_update_api'),
    path('api/artist/<int:pk>/delete/', views.artist_delete_api, name='artist_delete_api'),

    # 작품 API
    path('api/artwork/list/', views.artwork_list_api, name='artwork_list_api'),
    path('api/artwork/<int:pk>/', views.artwork_detail_api, name='artwork_detail_api'),
    path('api/artwork/create/', views.artwork_create_api, name='artwork_create_api'),
    path('api/artwork/<int:pk>/update/', views.artwork_update_api, name='artwork_update_api'),
    path('api/artwork/<int:pk>/delete/', views.artwork_delete_api, name='artwork_delete_api'),

    # 전시 API
    path('api/exhibition/list/', views.exhibition_list_api, name='exhibition_list_api'),
    path('api/exhibition/<int:pk>/', views.exhibition_detail_api, name='exhibition_detail_api'),
    path('api/exhibition/create/', views.exhibition_create_api, name='exhibition_create_api'),
    path('api/exhibition/<int:pk>/update/', views.exhibition_update_api, name='exhibition_update_api'),
    path('api/exhibition/<int:pk>/delete/', views.exhibition_delete_api, name='exhibition_delete_api'),

    # 인사말 API
    path('api/about/list/', views.about_list_api, name='about_list_api'),
    path('api/about/<int:pk>/', views.about_detail_api, name='about_detail_api'),
    path('api/about/create/', views.about_create_api, name='about_create_api'),
    path('api/about/<int:pk>/update/', views.about_update_api, name='about_update_api'),
    path('api/about/<int:pk>/delete/', views.about_delete_api, name='about_delete_api'),

    # 액자 API
    path('api/frame/list/', views.frame_list_api, name='frame_list_api'),
    path('api/frame/<int:pk>/', views.frame_detail_api, name='frame_detail_api'),
    path('api/frame/create/', views.frame_create_api, name='frame_create_api'),
    path('api/frame/<int:pk>/update/', views.frame_update_api, name='frame_update_api'),
    path('api/frame/<int:pk>/delete/', views.frame_delete_api, name='frame_delete_api'),

    # 연락처 API
    path('api/contact/list/', views.contact_list_api, name='contact_list_api'),
    path('api/contact/<int:pk>/', views.contact_detail_api, name='contact_detail_api'),
    path('api/contact/create/', views.contact_create_api, name='contact_create_api'),
    path('api/contact/<int:pk>/update/', views.contact_update_api, name='contact_update_api'),
    path('api/contact/<int:pk>/delete/', views.contact_delete_api, name='contact_delete_api'),

    # 홈 디자인 API
    path('api/home-design/current/', views.home_design_current_api, name='home_design_current_api'),
    path('api/home-design/switch/', views.home_design_switch_api, name='home_design_switch_api'),
]
