# HanaArt Gallery Django Project

## 운영서버 배포 가이드

### 1. 초기 설정 (최초 1회)

```bash
# 1. 프로젝트 디렉토리 생성
mkdir -p /var/www/hanaart
cd /var/www/hanaart

# 2. Docker 관련 파일 복사 (수동으로 복사 필요)
# - docker-compose.yml
# - docker/
# - .env
# - requirements.txt

# 3. 소스코드 클론
git clone https://github.com/hyuni75/hanaart.git src

# 4. 환경변수 설정
cp .env.example .env
vi .env  # 운영서버 설정으로 수정

# 5. Docker 컨테이너 시작
docker-compose up -d

# 6. 데이터베이스 마이그레이션 (중요!)
docker-compose exec web python manage.py migrate

# 7. 정적 파일 수집
docker-compose exec web python manage.py collectstatic --noinput

# 8. 슈퍼유저 생성
docker-compose exec web python manage.py createsuperuser

# 9. 초기 데이터 로드 (필요시)
docker-compose exec web python init_data.py         # 메뉴 데이터
docker-compose exec web python init_filter_data.py  # 필터 데이터  
docker-compose exec web python init_gallery_data.py # 갤러리 데이터 (작가, 전시, 작품)
```

### 2. 코드 업데이트 시

```bash
cd /var/www/hanaart

# 1. 최신 코드 가져오기
cd src
git pull origin main
cd ..

# 2. 마이그레이션 확인 및 실행
docker-compose exec web python manage.py showmigrations  # 마이그레이션 상태 확인
docker-compose exec web python manage.py migrate          # 마이그레이션 실행

# 3. 정적 파일 재수집 (필요시)
docker-compose exec web python manage.py collectstatic --noinput

# 4. 컨테이너 재시작
docker-compose restart
```

### 3. 마이그레이션 관련 명령어

```bash
# 마이그레이션 파일 생성 (개발서버에서만)
docker-compose exec web python manage.py makemigrations

# 마이그레이션 상태 확인
docker-compose exec web python manage.py showmigrations

# 특정 앱 마이그레이션
docker-compose exec web python manage.py migrate gallery
docker-compose exec web python manage.py migrate interaction
docker-compose exec web python manage.py migrate moderation
docker-compose exec web python manage.py migrate navigator
docker-compose exec web python manage.py migrate pagebuilder

# 마이그레이션 롤백 (특정 마이그레이션으로)
docker-compose exec web python manage.py migrate gallery 0001
```

### 4. 트러블슈팅

#### 마이그레이션 충돌 시
```bash
# 1. 현재 마이그레이션 상태 확인
docker-compose exec web python manage.py showmigrations

# 2. 가짜 마이그레이션 (이미 테이블이 있는 경우)
docker-compose exec web python manage.py migrate --fake

# 3. 특정 마이그레이션만 가짜로 적용
docker-compose exec web python manage.py migrate gallery 0001 --fake
```

#### 데이터베이스 초기화 (주의!)
```bash
# 1. 데이터베이스 백업
docker-compose exec db mysqldump -u root -p hanaart > backup.sql

# 2. 데이터베이스 삭제 및 재생성
docker-compose exec db mysql -u root -p -e "DROP DATABASE hanaart; CREATE DATABASE hanaart CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 3. 마이그레이션 재실행
docker-compose exec web python manage.py migrate
```

## 중요 사항

- **마이그레이션은 반드시 실행해야 합니다!** 
  - 새로운 모델이나 필드가 추가되었을 때
  - 기존 모델이 수정되었을 때
  
- **마이그레이션 파일은 Git에 포함되어 있습니다**
  - `apps/*/migrations/*.py` 파일들
  - 개발서버와 운영서버가 동일한 마이그레이션 사용

- **운영서버에서는 makemigrations 실행하지 마세요**
  - 마이그레이션 파일은 개발서버에서만 생성
  - 운영서버는 migrate만 실행