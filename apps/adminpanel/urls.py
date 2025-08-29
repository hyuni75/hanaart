from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "adminpanel"

urlpatterns = [
    # 로그인/로그아웃
    path("login/", auth_views.LoginView.as_view(
        template_name="adminpanel/login.html",
        redirect_authenticated_user=True
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(
        next_page="/"
    ), name="logout"),
    
    # 메인 대시보드  
    path("", views.dashboard, name="dashboard"),
]
