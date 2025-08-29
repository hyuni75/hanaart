# HanaArt 관리 시스템 구조 (Manage System)

## ⚠️ 중요: 이 문서를 항상 먼저 참조하세요!

## 1. URL 구조 정리

### 메인 URL 라우팅 (config/urls.py)
```python
path('', include('apps.gallery.urls')),  # gallery 앱이 루트에 포함됨
path('', include('apps.adminpanel.urls')),  # adminpanel 앱도 루트에 포함됨
```

### 실제 관리 페이지 URL 매핑
```
/manage/ → adminpanel 앱 → dashboard
/manage/artists/ → 리다이렉트 → gallery:artist_manage_list
/manage/artworks/ → 리다이렉트 → gallery:artwork_manage_list  
/manage/exhibitions/ → 리다이렉트 → gallery:exhibition_manage_list
```

## 2. 삭제 기능 URL 매핑 (핵심!)

### 작품 (Artwork) 삭제
```
템플릿: templates/admin/artwork_list.html
onclick: deleteArtwork(id, title)
JavaScript: fetch(`/admin/artworks/${id}/delete/`)
URL 패턴: gallery/urls.py → path('admin/artworks/<int:pk>/delete/', views.artwork_delete)
View: apps/gallery/views.py → artwork_delete(request, pk)
```

### 작가 (Artist) 삭제
```
템플릿: templates/admin/artist_list.html
onclick: deleteArtist(id, name)
JavaScript: fetch(`/admin/artists/${id}/delete/`)
URL 패턴: gallery/urls.py → path('admin/artists/<int:pk>/delete/', views.artist_delete)
View: apps/gallery/views.py → artist_delete(request, pk)
```

### 전시 (Exhibition) 삭제
```
템플릿: templates/admin/exhibition_list.html
onclick: deleteExhibition(id, title)
JavaScript: fetch(`/admin/exhibitions/${id}/delete/`)
URL 패턴: gallery/urls.py → path('admin/exhibitions/<int:pk>/delete/', views.exhibition_delete)
View: apps/gallery/views.py → exhibition_delete(request, pk)
```

## 3. CRUD 전체 URL 패턴

### Artist CRUD
```
LIST:   /admin/artists/ → artist_manage_list
CREATE: /admin/artists/create/ → artist_create
EDIT:   /admin/artists/{id}/edit/ → artist_edit
DELETE: /admin/artists/{id}/delete/ → artist_delete
```

### Artwork CRUD
```
LIST:   /admin/artworks/ → artwork_manage_list
CREATE: /admin/artworks/create/ → artwork_create
EDIT:   /admin/artworks/{id}/edit/ → artwork_edit
DELETE: /admin/artworks/{id}/delete/ → artwork_delete
```

### Exhibition CRUD
```
LIST:   /admin/exhibitions/ → exhibition_manage_list
CREATE: /admin/exhibitions/create/ → exhibition_create
EDIT:   /admin/exhibitions/{id}/edit/ → exhibition_edit
DELETE: /admin/exhibitions/{id}/delete/ → exhibition_delete
CURRENT: /admin/exhibitions/{id}/set-current/ → exhibition_set_current
```

## 4. JavaScript 함수와 View 연결

### 공통 패턴
```javascript
function delete{Model}(id, title) {
    hanaModal.confirmDelete(title, function() {
        fetch(`/admin/{models}/${id}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
    });
}
```

### View 응답 패턴
```python
@login_required
@require_POST
def {model}_delete(request, pk):
    obj = get_object_or_404(Model, pk=pk)
    obj.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': '삭제되었습니다.'})
    return redirect('gallery:{model}_manage_list')
```

## 5. 템플릿 위치

### 관리 페이지 템플릿
```
templates/admin/
├── base_admin.html (베이스 템플릿, getCookie 함수 정의)
├── gallery_dashboard.html (대시보드)
├── artist_list.html (작가 목록)
├── artist_form.html (작가 생성/수정)
├── artwork_list.html (작품 목록)
├── artwork_form.html (작품 생성/수정)
├── exhibition_list.html (전시 목록)
└── exhibition_form.html (전시 생성/수정)
```

## 6. 주의사항

### ❌ 자주 하는 실수
1. JavaScript URL에 `/gallery/` 접두사 추가 (잘못됨)
2. Django Admin (`/admin/`)과 커스텀 관리 페이지(`/manage/`) 혼동
3. URL 패턴과 JavaScript fetch URL 불일치

### ✅ 올바른 패턴
1. JavaScript URL: `/admin/{model}s/{id}/{action}/`
2. URL 패턴: `admin/{model}s/<int:pk>/{action}/`
3. gallery 앱이 루트에 포함되므로 `/gallery/` 접두사 불필요

## 7. 디버깅 체크리스트

문제 발생 시 확인 순서:
1. [ ] JavaScript 콘솔 에러 확인
2. [ ] Network 탭에서 404 에러 확인
3. [ ] JavaScript fetch URL 확인
4. [ ] gallery/urls.py의 URL 패턴 확인
5. [ ] View 함수의 데코레이터 확인 (@login_required, @require_POST)
6. [ ] CSRF 토큰 확인
7. [ ] Docker 재시작

## 8. 빠른 참조

### 작품 삭제가 안 될 때
```javascript
// 확인: templates/admin/artwork_list.html
// 올바른 URL: /admin/artworks/${id}/delete/
// 잘못된 URL: /gallery/admin/artworks/${id}/delete/
```

### 작가 삭제가 안 될 때
```javascript
// 확인: templates/admin/artist_list.html
// 올바른 URL: /admin/artists/${id}/delete/
// 잘못된 URL: /gallery/admin/artists/${id}/delete/
```

---
*이 문서는 manage 시스템의 URL 구조를 명확히 정리한 것입니다.*
*문제 해결 시 이 문서를 먼저 참조하세요!*
*최종 업데이트: 2025-08-29*