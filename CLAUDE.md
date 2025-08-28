# HanaArt Django 프로젝트 개발 가이드

## 프로젝트 개요
- **개발자 호칭**: 제로님
- **프레임워크**: Django MVT + MariaDB + Docker Compose
- **개발 방식**: 전형적인 CRUD 로직 기반
- **URL**: http://192.168.100.10:8086/

## 시스템 아키텍처
- **Backend**: Django Framework (MVT Pattern)
- **Database**: MariaDB
- **Container**: Docker Compose
- **Frontend**: Django Templates

## 디렉토리 구조

### 루트 디렉토리 (/home/hyuni/hanaart/)
```
.env                    # 환경변수 설정
.gitignore             # Git 제외 파일
Makefile               # 빌드 자동화
cleanup_project.sh     # 프로젝트 정리 스크립트
docker/                # Docker 설정 파일
docker-compose.yml     # Docker Compose 설정
load-env.sh           # 환경변수 로드 스크립트
optimize-centos7.sh   # CentOS 7 최적화 스크립트
requirements.txt      # Python 패키지 목록
src/                  # Django 앱 소스 코드 (Git 관리 대상)
```

### src 디렉토리 구조
```
apps/          # Django 앱들이 위치할 디렉토리
config/        # Django 설정 파일
  - __init__.py
  - asgi.py
  - settings.py    # 메인 설정 파일
  - urls.py        # URL 라우팅
  - wsgi.py
  - settings/      # 추가 설정 디렉토리
logs/          # 로그 파일
main/          # 메인 앱
manage.py      # Django 관리 스크립트
media/         # 미디어 파일 저장소
run/           # 실행 관련 파일
secrets.json   # 비밀 키 및 민감 정보
static/        # 정적 파일
staticfiles/   # 수집된 정적 파일
templates/     # 모든 템플릿 파일 (앱별 분리 없이 직접 저장)
```

## 개발 규칙

### 1. 앱 생성 및 관리
- 새로운 Django 앱은 `apps/` 디렉토리에 생성
- 모든 템플릿은 `templates/` 디렉토리에 직접 저장 (앱별 분리 없음)

### 2. UI/UX 일관성
- 기본 브라우저 알람창이나 모달 사용 금지
- 공통 모달창과 공통 토스트창을 사전 정의하여 사용
- 일관된 사용자 경험 제공

### 3. 코드 변경 후 필수 작업
- 프론트엔드/백엔드 코드 추가, 수정, 삭제 시 반드시 실행:
  ```bash
  docker compose restart
  ```

### 4. Git 관리
- Git 관리 범위: `src/` 폴더만
- Repository: https://github.com/hyuni75/hanaart.git
- Branch: main

### Git 초기 설정 명령어
```bash
echo "# hanaart" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/hyuni75/hanaart.git
git push -u origin main
```

## 서버 환경
- 개발 서버: 현재 시스템
- 운영 서버: 동일한 폴더 구조로 구성

## 중요 사항
1. 세션 초기화 시 이 파일을 필수적으로 읽어 개발 시스템 숙지
2. Django MVT 패턴 준수
3. CRUD 로직 중심의 개발
4. Docker Compose 기반 컨테이너 환경
5. MariaDB 데이터베이스 사용

---
*이 문서는 HanaArt 프로젝트의 개발 가이드라인입니다.*