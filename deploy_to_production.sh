#!/bin/bash

# 운영서버 배포 스크립트
# 실행 방법: bash deploy_to_production.sh

echo "========================================="
echo "하나아트갤러리 운영서버 배포 시작"
echo "========================================="

# 1. Git 최신 코드 받기
echo ""
echo "[1/4] Git Pull - 최신 코드 받기..."
git pull origin main

if [ $? -ne 0 ]; then
    echo "❌ Git pull 실패!"
    exit 1
fi
echo "✅ 최신 코드 업데이트 완료"

# 2. 마이그레이션 실행
echo ""
echo "[2/4] 데이터베이스 마이그레이션 실행..."
cd ..
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

if [ $? -ne 0 ]; then
    echo "❌ 마이그레이션 실패!"
    exit 1
fi
echo "✅ 마이그레이션 완료"

# 3. 초기 작가 데이터 로드
echo ""
echo "[3/4] 초기 작가 데이터 로드..."
docker compose exec web python load_initial_artists.py

if [ $? -ne 0 ]; then
    echo "⚠️ 초기 데이터 로드 실패 (이미 데이터가 있을 수 있음)"
else
    echo "✅ 초기 작가 데이터 로드 완료"
fi

# 4. Docker 컨테이너 재시작
echo ""
echo "[4/4] Docker 컨테이너 재시작..."
docker compose restart

if [ $? -ne 0 ]; then
    echo "❌ Docker 재시작 실패!"
    exit 1
fi

echo ""
echo "========================================="
echo "✅ 운영서버 배포 완료!"
echo "========================================="
echo ""
echo "다음 항목들이 업데이트되었습니다:"
echo "- 현재전시 관리 기능 (CurrentExhibition)"
echo "- 전속작가 관리 기능 (SimpleArtist)"
echo "- 물리적 페이지 라우팅"
echo "- 초기 작가 데이터 (6명)"
echo ""
echo "브라우저에서 http://192.168.100.10:8086/ 로 확인하세요."