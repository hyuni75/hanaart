from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "adminpanel"

urlpatterns = [
    # 로그인/로그아웃
    path("manage/login/", auth_views.LoginView.as_view(
        template_name="adminpanel/login.html",
        redirect_authenticated_user=True
    ), name="login"),
    path("manage/logout/", auth_views.LogoutView.as_view(
        next_page="/"
    ), name="logout"),
    
    # 메인 대시보드  
    path("manage/", views.dashboard, name="dashboard"),
    
    # 작가 관리를 gallery 앱으로 리다이렉트
    path("manage/artists/", views.redirect_to_artist_list, name="artist_list"),
    path("manage/exhibitions/", views.redirect_to_exhibition_list, name="exhibition_list"),
    path("manage/artworks/", views.redirect_to_artwork_list, name="artwork_list"),
]
