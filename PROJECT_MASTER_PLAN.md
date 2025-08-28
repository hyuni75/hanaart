# 하나아트갤러리 동적 웹사이트 관리 시스템 - 마스터 플랜

## 📋 프로젝트 개요
- **프로젝트명**: HanaArt Dynamic CMS
- **목표**: 일반 관리자가 코드 없이 관리 가능한 동적 웹사이트 시스템
- **기술스택**: Django MVT + MariaDB + Docker Compose
- **URL**: http://192.168.100.10:8086/

## 🏗️ Django 앱 구조

### apps/ 디렉토리 구조
```
apps/
├── core/           # 핵심 기능 및 공통 모듈
├── navigator/      # 네비게이션 관리 시스템
├── pagebuilder/    # 페이지 빌더 시스템
├── gallery/        # 갤러리 전용 기능
├── interaction/    # 상호작용 시스템 (댓글, 좋아요)
└── moderation/     # 콘텐츠 필터링 및 관리
```

## 📊 작업 단계별 계획

### Phase 1: 기초 설정 (Week 1)
| 번호 | 작업 내용 | 상태 | 비고 |
|------|-----------|------|------|
| 1.1 | 기존 생성된 앱 정리 | ⏳ | webmanager, cms 등 정리 필요 |
| 1.2 | Django 앱 생성 (core) | ⏳ | 인증, 권한, 공통 기능 |
| 1.3 | Django 앱 생성 (navigator) | ⏳ | 네비게이션 관리 |
| 1.4 | Django 앱 생성 (pagebuilder) | ⏳ | 페이지 빌더 |
| 1.5 | Django 앱 생성 (gallery) | ⏳ | 갤러리 기능 |
| 1.6 | Django 앱 생성 (interaction) | ⏳ | 상호작용 기능 |
| 1.7 | Django 앱 생성 (moderation) | ⏳ | 콘텐츠 검증 |
| 1.8 | settings.py 설정 | ⏳ | INSTALLED_APPS 등록 |

### Phase 2: 데이터 모델링 (Week 2)
| 번호 | 작업 내용 | 상태 | 비고 |
|------|-----------|------|------|
| 2.1 | core 모델 설계 | ⏳ | User 확장, BaseModel |
| 2.2 | navigator 모델 설계 | ⏳ | MenuItem, MenuGroup |
| 2.3 | pagebuilder 모델 설계 | ⏳ | Page, Block, Template |
| 2.4 | gallery 모델 설계 | ⏳ | Artist, Exhibition, Artwork |
| 2.5 | interaction 모델 설계 | ⏳ | Comment, Like, Rating |
| 2.6 | moderation 모델 설계 | ⏳ | FilterRule, BlockedWord |
| 2.7 | 모델 마이그레이션 | ⏳ | makemigrations & migrate |

### Phase 3: 관리자 시스템 (Week 3)
| 번호 | 작업 내용 | 상태 | 비고 |
|------|-----------|------|------|
| 3.1 | 관리자 대시보드 템플릿 | ⏳ | templates/admin/ |
| 3.2 | 네비게이션 관리 UI | ⏳ | 드래그&드롭 |
| 3.3 | 페이지 빌더 UI | ⏳ | WYSIWYG 에디터 |
| 3.4 | 미디어 관리 UI | ⏳ | 이미지 업로드/관리 |
| 3.5 | 상호작용 관리 UI | ⏳ | 댓글/좋아요 관리 |
| 3.6 | 콘텐츠 필터 설정 UI | ⏳ | 금지어 관리 |

### Phase 4: 사용자 인터페이스 (Week 4)
| 번호 | 작업 내용 | 상태 | 비고 |
|------|-----------|------|------|
| 4.1 | 베이스 템플릿 | ⏳ | templates/base.html |
| 4.2 | 네비게이션 템플릿 | ⏳ | 동적 메뉴 렌더링 |
| 4.3 | 페이지 템플릿 | ⏳ | 블록 기반 렌더링 |
| 4.4 | 갤러리 템플릿 | ⏳ | 작가/전시/작품 |
| 4.5 | 상호작용 컴포넌트 | ⏳ | 댓글/좋아요 위젯 |

### Phase 5: 기능 구현 (Week 5-6)
| 번호 | 작업 내용 | 상태 | 비고 |
|------|-----------|------|------|
| 5.1 | 사용자 인증 시스템 | ⏳ | 로그인/권한 |
| 5.2 | 동적 메뉴 시스템 | ⏳ | 순서변경/활성화 |
| 5.3 | 페이지 빌더 엔진 | ⏳ | 블록 렌더링 |
| 5.4 | 미디어 처리 | ⏳ | 썸네일 생성 |
| 5.5 | 댓글 시스템 | ⏳ | AJAX 기반 |
| 5.6 | 좋아요 시스템 | ⏳ | 실시간 업데이트 |
| 5.7 | 콘텐츠 필터링 | ⏳ | 실시간 검증 |

### Phase 6: 테스트 및 배포 (Week 7)
| 번호 | 작업 내용 | 상태 | 비고 |
|------|-----------|------|------|
| 6.1 | 단위 테스트 작성 | ⏳ | pytest |
| 6.2 | 통합 테스트 | ⏳ | 전체 플로우 |
| 6.3 | 성능 최적화 | ⏳ | 캐싱, 쿼리 최적화 |
| 6.4 | 보안 점검 | ⏳ | XSS, CSRF 등 |
| 6.5 | Docker 컨테이너 최적화 | ⏳ | 이미지 크기 감소 |
| 6.6 | 배포 준비 | ⏳ | 운영 환경 설정 |

## 🔧 상호작용 시스템 설계

### 댓글 시스템
- **기능**: 게시물별 댓글, 대댓글, 수정/삭제
- **권한**: 회원/비회원 구분, 작성자 본인만 수정/삭제
- **알림**: 댓글 알림 시스템

### 좋아요 시스템
- **기능**: 게시물/댓글 좋아요
- **제한**: 중복 방지, 회원 전용
- **통계**: 실시간 카운트

### 적용 범위 설정
- **레벨 1**: 개별 게시물 단위 on/off
- **레벨 2**: 메뉴(카테고리) 단위 on/off
- **레벨 3**: 시스템 전체 on/off

## 🛡️ 콘텐츠 필터링 시스템

### 필터링 대상
1. **욕설/비속어**: 사전 기반 필터링
2. **광고성 콘텐츠**: URL 패턴 감지
3. **개인정보**: 전화번호, 이메일 패턴
4. **스팸**: 반복 문자, 과도한 특수문자

### 필터링 액션
- **차단**: 등록 거부
- **대체**: 별표(*) 처리
- **검토**: 관리자 승인 대기
- **경고**: 사용자 경고 메시지

### 필터 규칙 관리
```python
# moderation/models.py
class FilterRule(models.Model):
    ACTIONS = [
        ('block', '차단'),
        ('replace', '대체'),
        ('review', '검토'),
        ('warning', '경고'),
    ]
    pattern = models.CharField(max_length=200)
    action = models.CharField(max_length=20, choices=ACTIONS)
    is_regex = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
```

## 📁 파일 구조 규칙

### Django 앱 위치
```
src/apps/
└── [앱이름]/
    ├── __init__.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── apps.py
```

### 템플릿 위치
```
src/templates/
├── base.html
├── admin/
│   └── [관리자 템플릿]
├── [앱이름]/
│   └── [앱별 템플릿]
└── components/
    └── [재사용 컴포넌트]
```

## 🔄 세션 연속성 보장

### 진행 상태 기록
- 각 Phase별 진행률 기록
- 완료된 작업 체크
- 다음 작업 명시

### 참조 문서
1. `/home/hyuni/hanaart/src/CLAUDE.md` - 프로젝트 기본 정보
2. `/home/hyuni/hanaart/src/PROJECT_MASTER_PLAN.md` - 이 문서 (마스터 플랜)
3. `/home/hyuni/hanaart/src/WORK_PROGRESS.md` - 작업 진행 상태

## 🎯 다음 단계 작업
1. 기존 생성된 앱 정리 (cms, webmanager, sitemanager, gallery)
2. apps/ 폴더 구조에 맞게 재배치
3. Phase 1.2부터 순차 진행

---
*마지막 업데이트: 2025-08-28*
*상태: Phase 1 준비 중*