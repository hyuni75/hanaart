# HanaArt Django 앱 구조 가이드

## 현재 구현된 앱 목록

### 1. Core 앱 (`apps/core/`)
**목적**: 공통 기능 및 베이스 모델 제공
- `TimeStampedModel`: created_at, updated_at 필드를 제공하는 추상 모델
- 모든 모델이 이를 상속받아 생성/수정 시간 자동 관리

### 2. Navigator 앱 (`apps/navigator/`)
**목적**: 메인 네비게이션 및 정적 페이지 관리
- **Views**: IndexView, GalleryView, ArtistView, ExhibitionView, NewsView, ContactView, AboutView
- **Templates**: index.html, gallery.html, artist.html, exhibition.html, news.html, contact.html, about.html
- **Context Processor**: 전역 메뉴 아이템 제공
- **URL Prefix**: `/` (루트)

### 3. Gallery 앱 (`apps/gallery/`)
**목적**: 작품, 작가, 전시 관리 (핵심 비즈니스 로직)

#### 모델 구조
```python
Artist:
  - name (작가명)
  - profile_image (프로필 이미지)
  - bio, education, awards (약력 정보)
  - is_exclusive (전속작가 여부)
  - is_active (활성화 상태)

Exhibition:
  - title (전시명)
  - exhibition_type (개인전/단체전/특별전/아트페어)
  - artists (ManyToMany)
  - start_date, end_date (전시 기간)
  - is_current, is_featured, is_published (상태 플래그)

Artwork:
  - title (작품명)
  - artist (ForeignKey → Artist)
  - artwork_type (회화/조각/사진 등)
  - main_image, thumbnail (이미지)
  - price, is_sold, is_for_sale (판매 정보)
  - exhibitions (ManyToMany)

ArtworkImage:
  - artwork (ForeignKey → Artwork)
  - image (추가 이미지)
  - caption, order (캡션과 순서)
```

#### ImageOptimizer 유틸리티
- 썸네일 생성 (300x300)
- 중간 크기 생성 (800x800)
- 대형 이미지 최적화 (1920x1920)
- 반응형 이미지 세트 생성

### 4. AdminPanel 앱 (`apps/adminpanel/`)
**목적**: 커스텀 관리자 대시보드
- **Views**: DashboardView, ManageView, ActionView
- **Templates**: admin/dashboard.html, admin/manage_*.html
- **기능**: 
  - 통계 대시보드
  - AJAX 기반 삭제/토글 작업
  - 커스텀 관리 인터페이스
- **URL Prefix**: `/adminpanel/`

### 5. Interaction 앱 (`apps/interaction/`)
**목적**: 사용자 상호작용 기능
- Contact 모델 (연락처 폼 제출)
- NewsletterSubscriber 모델 (뉴스레터 구독)
- **기능**: 폼 제출, 구독 관리

### 6. Moderation 앱 (`apps/moderation/`)
**목적**: 콘텐츠 검토 및 승인
- ContentReview 모델
- **상태**: pending, approved, rejected
- **기능**: 콘텐츠 검토 워크플로우

### 7. PageBuilder 앱 (`apps/pagebuilder/`)
**목적**: 동적 페이지 생성
- Page 모델 (동적 페이지)
- PageSection 모델 (페이지 섹션)
- **기능**: CMS 스타일 페이지 관리

## 앱 간 의존성

```
Core (베이스)
  ↓
Gallery (핵심 비즈니스)
  ↓
Navigator (프론트엔드 표시)
  ↓
AdminPanel (관리 인터페이스)

Interaction → Gallery (작품 문의)
Moderation → Gallery (콘텐츠 검토)
PageBuilder (독립적)
```

## 앱 생성 템플릿

새 앱을 추가할 때 사용할 구조:

```bash
# 앱 생성
python manage.py startapp appname apps/appname

# 필수 파일 구조
apps/appname/
├── __init__.py
├── admin.py          # Django Admin 설정
├── apps.py           # 앱 설정
├── models.py         # 데이터 모델
├── views.py          # 뷰 로직
├── urls.py           # URL 패턴
├── forms.py          # 폼 클래스 (필요시)
├── serializers.py    # API 시리얼라이저 (필요시)
├── utils.py          # 유틸리티 함수
├── migrations/       # 마이그레이션 파일
└── tests.py          # 테스트 코드
```

## 모델 작성 규칙

```python
from apps.core.models import TimeStampedModel

class MyModel(TimeStampedModel):
    """모델 설명"""
    # 필드 정의
    name = models.CharField(max_length=100, verbose_name='이름')
    
    # 관계 필드
    related_model = models.ForeignKey(
        'OtherModel',
        on_delete=models.CASCADE,
        related_name='mymodels',
        verbose_name='관련 모델'
    )
    
    # 상태 필드
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    
    class Meta:
        verbose_name = '모델명'
        verbose_name_plural = '모델명 목록'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
```

## View 작성 규칙

### 함수 기반 뷰 (FBV)
```python
def model_list(request):
    objects = Model.objects.filter(is_active=True)
    context = {
        'object_list': objects,
        'page_title': '목록',
    }
    return render(request, 'model_list.html', context)
```

### 클래스 기반 뷰 (CBV)
```python
from django.views.generic import ListView

class ModelListView(ListView):
    model = Model
    template_name = 'model_list.html'
    context_object_name = 'objects'
    paginate_by = 20
    
    def get_queryset(self):
        return Model.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '목록'
        return context
```

## URL 패턴 규칙

```python
from django.urls import path
from . import views

app_name = 'appname'

urlpatterns = [
    path('', views.ModelListView.as_view(), name='model-list'),
    path('<int:pk>/', views.ModelDetailView.as_view(), name='model-detail'),
    path('create/', views.ModelCreateView.as_view(), name='model-create'),
    path('<int:pk>/update/', views.ModelUpdateView.as_view(), name='model-update'),
    path('<int:pk>/delete/', views.ModelDeleteView.as_view(), name='model-delete'),
]
```

## Admin 등록 규칙

```python
from django.contrib import admin
from .models import Model

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'description')
        }),
        ('상태', {
            'fields': ('is_active',)
        }),
    )
```

## 마이그레이션 관리

```bash
# 마이그레이션 생성
python manage.py makemigrations appname

# 마이그레이션 적용
python manage.py migrate

# 마이그레이션 확인
python manage.py showmigrations

# 특정 마이그레이션으로 롤백
python manage.py migrate appname 0001
```

## 테스트 작성 규칙

```python
from django.test import TestCase
from django.urls import reverse
from .models import Model

class ModelTestCase(TestCase):
    def setUp(self):
        self.obj = Model.objects.create(name='Test')
    
    def test_model_creation(self):
        self.assertEqual(self.obj.name, 'Test')
    
    def test_list_view(self):
        response = self.client.get(reverse('appname:model-list'))
        self.assertEqual(response.status_code, 200)
```

## 정적 파일 구조

```
static/
├── css/
│   ├── base.css         # 공통 스타일
│   └── appname.css       # 앱별 스타일
├── js/
│   ├── base.js          # 공통 스크립트
│   └── appname.js       # 앱별 스크립트
└── images/
    └── appname/          # 앱별 이미지
```

## 개발 체크리스트

새 기능 추가 시:
- [ ] 모델 정의 및 마이그레이션
- [ ] Admin 등록
- [ ] URL 패턴 추가
- [ ] View 작성
- [ ] Template 생성
- [ ] 정적 파일 추가
- [ ] 테스트 작성
- [ ] Docker 재시작
- [ ] 기능 테스트

---
*이 문서는 HanaArt 프로젝트의 앱 구조를 설명합니다.*
*최종 업데이트: 2025-08-29*