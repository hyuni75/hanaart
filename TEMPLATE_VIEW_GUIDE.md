# HanaArt Django 템플릿-뷰 연결 가이드

## 1. URL 라우팅 구조

### 메인 URL 설정 (config/urls.py)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminpanel/', include('apps.adminpanel.urls')),
    path('gallery/', include('apps.gallery.urls')),
    path('interaction/', include('apps.interaction.urls')),
    path('', include('apps.navigator.urls')),
]
```

### URL 네임스페이스 규칙
- 각 앱은 고유한 네임스페이스 사용
- 형식: `app_name:view_name`
- 예: `gallery:artwork_detail`, `adminpanel:dashboard`

## 2. View-Template 매핑 패턴

### 기본 렌더링 패턴
```python
def view_name(request):
    context = {
        'key': 'value',
    }
    return render(request, 'template_name.html', context)
```

### 현재 구현된 View-Template 매핑

#### Navigator 앱 (메인 페이지)
- `IndexView` → `index.html`
- `GalleryView` → `gallery.html`
- `ArtistView` → `artist.html`
- `ExhibitionView` → `exhibition.html`
- `NewsView` → `news.html`
- `ContactView` → `contact.html`
- `AboutView` → `about.html`

#### Gallery 앱 (CRUD 작업)
- `ArtworkListView` → `gallery/artwork_list.html`
- `ArtworkDetailView` → `gallery/artwork_detail.html`
- `ArtworkCreateView` → `gallery/artwork_form.html`
- `ArtworkUpdateView` → `gallery/artwork_form.html`
- `ArtworkDeleteView` → `gallery/artwork_delete.html`

#### AdminPanel 앱 (관리자)
- `DashboardView` → `admin/dashboard.html`
- `ManageView` → `admin/manage_[model].html`
- `ActionView` → AJAX 응답 (JSON)

## 3. 템플릿 디렉토리 구조

```
templates/
├── base.html                 # 사용자 페이지 베이스
├── index.html                # 메인 페이지
├── gallery.html              # 갤러리 목록
├── artist.html               # 작가 목록
├── exhibition.html           # 전시 목록
├── news.html                 # 뉴스 목록
├── contact.html              # 연락처
├── about.html                # 소개
├── admin/
│   ├── base_admin.html      # 관리자 페이지 베이스
│   ├── dashboard.html        # 대시보드
│   ├── manage_artworks.html # 작품 관리
│   ├── manage_artists.html  # 작가 관리
│   └── manage_exhibitions.html # 전시 관리
├── gallery/
│   ├── artwork_list.html    # 작품 목록
│   ├── artwork_detail.html  # 작품 상세
│   └── artwork_form.html    # 작품 폼
└── components/
    ├── modal.html            # 공통 모달
    └── toast.html            # 공통 토스트
```

## 4. 템플릿 상속 구조

### 사용자 페이지
```django
{% extends 'base.html' %}
{% block title %}페이지 제목{% endblock %}
{% block content %}
    <!-- 페이지 컨텐츠 -->
{% endblock %}
```

### 관리자 페이지
```django
{% extends 'admin/base_admin.html' %}
{% block title %}관리자 - 페이지 제목{% endblock %}
{% block content %}
    <!-- 관리자 페이지 컨텐츠 -->
{% endblock %}
```

## 5. 컨텍스트 데이터 전달 패턴

### 기본 컨텍스트 구조
```python
context = {
    'object_list': queryset,      # 목록 뷰
    'object': instance,            # 상세 뷰
    'form': form_instance,         # 폼 뷰
    'page_title': '페이지 제목',
    'breadcrumb': [...],          # 빵부스러기 네비게이션
}
```

### 글로벌 컨텍스트 프로세서
- `menu_items`: 모든 페이지에서 사용 가능한 메뉴 아이템
- 위치: `apps/navigator/context_processors.py`

## 6. AJAX 패턴

### AJAX 요청 처리
```python
@require_http_methods(["POST"])
def ajax_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX 처리
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
```

### 현재 구현된 AJAX 엔드포인트
- `/adminpanel/action/delete/` - 삭제 작업
- `/adminpanel/action/toggle/` - 토글 작업 (활성화/비활성화)

## 7. 개발 규칙

### 템플릿 네이밍
- 목록 뷰: `model_list.html`
- 상세 뷰: `model_detail.html`
- 폼 뷰: `model_form.html`
- 삭제 확인: `model_delete.html`

### View 네이밍
- 목록: `ModelListView`
- 상세: `ModelDetailView`
- 생성: `ModelCreateView`
- 수정: `ModelUpdateView`
- 삭제: `ModelDeleteView`

### URL 패턴 네이밍
- 목록: `model-list`
- 상세: `model-detail`
- 생성: `model-create`
- 수정: `model-update`
- 삭제: `model-delete`

## 8. 공통 컴포넌트 사용

### 모달 사용법
```django
{% include 'components/modal.html' with modal_id="myModal" modal_title="제목" modal_body="내용" %}
```

### 토스트 사용법
```django
{% include 'components/toast.html' with message="메시지" type="success" %}
```

## 9. 정적 파일 처리

### CSS/JS 파일 위치
- 개발: `static/css/`, `static/js/`
- 배포: `staticfiles/` (collectstatic 후)

### 템플릿에서 정적 파일 사용
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/main.js' %}"></script>
```

## 10. 미디어 파일 처리

### 업로드 경로
- 작가 프로필: `media/artists/profiles/`
- 작품 이미지: `media/artworks/`
- 전시 포스터: `media/exhibitions/posters/`

### 템플릿에서 미디어 파일 사용
```django
{% if object.image %}
    <img src="{{ object.image.url }}" alt="{{ object.title }}">
{% endif %}
```

## 11. 폼 처리 패턴

### 기본 폼 뷰
```python
class ModelCreateView(CreateView):
    model = Model
    form_class = ModelForm
    template_name = 'model_form.html'
    success_url = reverse_lazy('app:model-list')
    
    def form_valid(self, form):
        # 추가 처리
        return super().form_valid(form)
```

### 템플릿에서 폼 렌더링
```django
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">저장</button>
</form>
```

## 12. 에러 처리

### 404 페이지
- 템플릿: `templates/404.html`
- 자동으로 Django가 처리

### 500 페이지
- 템플릿: `templates/500.html`
- 프로덕션 환경에서만 표시

## 13. 보안 고려사항

### CSRF 보호
- 모든 POST 폼에 `{% csrf_token %}` 필수
- AJAX 요청 시 CSRF 토큰 헤더 포함

### XSS 방지
- 사용자 입력은 자동 이스케이프
- 안전한 HTML 출력 시: `{{ content|safe }}`

## 14. 개발 워크플로우

### 새 기능 추가 순서
1. Model 정의 (`models.py`)
2. URL 패턴 추가 (`urls.py`)
3. View 작성 (`views.py`)
4. Template 생성 (`templates/`)
5. 정적 파일 추가 (필요시)
6. 마이그레이션 실행
7. Docker 재시작

### 코드 변경 후 필수 작업
```bash
docker compose restart
```

---
*이 문서는 HanaArt 프로젝트의 템플릿-뷰 연결 구조를 설명합니다.*
*최종 업데이트: 2025-08-29*