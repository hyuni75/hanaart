# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def index(request):
    return JsonResponse({
        'project': settings.PROJECT_NAME,
        'version': settings.PROJECT_VERSION,
        'status': 'healthy',
        'language': settings.LANGUAGE_CODE,
        'timezone': settings.TIME_ZONE,
        'debug': settings.DEBUG,
        'message': '🚀 Django 프로젝트가 성공적으로 실행중입니다!'
    }, json_dumps_params={'ensure_ascii': False})

def health_check(request):
    return JsonResponse({'status': 'healthy'})

urlpatterns = [
    # 프론트엔드 페이지 URL
    path('', include('apps.pages.urls')),           # 홈, 인사말, 연혁, 연락처
    path('', include('apps.gallery.urls')),         # 전시, 아트페어, 작가, 액자제작

    # 관리자 페이지 URL
    path('admin-panel/', include('apps.admin_panel.urls')),  # 관리자 CRUD

    # Django 기본 관리자
    path('admin/', admin.site.urls),

    # API 엔드포인트
    path('api/', include('rest_framework.urls')),

    # 헬스 체크
    path('health/', health_check, name='health_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('silk/', include('silk.urls', namespace='silk')),
    ] + urlpatterns

admin.site.site_header = f'{settings.PROJECT_NAME} 관리'
admin.site.site_title = f'{settings.PROJECT_NAME}'
admin.site.index_title = '관리 홈'
