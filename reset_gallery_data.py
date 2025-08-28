#!/usr/bin/env python
"""
갤러리 데이터 초기화 스크립트
User 모델을 제외한 모든 갤러리 관련 데이터를 삭제하고 시퀀스를 리셋합니다.
"""

import os
import sys
import django
from django.db import connection

# Django 설정
sys.path.insert(0, '/home/hyuni/hanaart/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.gallery.models import Artist, Exhibition, Artwork, ArtworkImage
from django.core.files.storage import default_storage
import shutil

def reset_gallery_data():
    """갤러리 데이터 초기화"""
    
    print("=" * 60)
    print("갤러리 데이터 초기화를 시작합니다...")
    print("주의: User 모델을 제외한 모든 갤러리 데이터가 삭제됩니다!")
    print("=" * 60)
    
    # 확인 프롬프트
    confirm = input("\n정말로 계속하시겠습니까? (yes/no): ")
    if confirm.lower() != 'yes':
        print("취소되었습니다.")
        return
    
    try:
        # 1. 외래키 제약조건을 고려한 순서대로 삭제
        print("\n1. 작품 추가 이미지 삭제...")
        artwork_images = ArtworkImage.objects.all()
        for img in artwork_images:
            if img.image and default_storage.exists(img.image.name):
                default_storage.delete(img.image.name)
        artwork_images.delete()
        print(f"   - {ArtworkImage.objects.count()} 개 삭제 완료")
        
        print("\n2. 작품 데이터 삭제...")
        artworks = Artwork.objects.all()
        for artwork in artworks:
            # 메인 이미지 삭제
            if artwork.main_image and default_storage.exists(artwork.main_image.name):
                default_storage.delete(artwork.main_image.name)
            # 썸네일 삭제
            if artwork.thumbnail and default_storage.exists(artwork.thumbnail.name):
                default_storage.delete(artwork.thumbnail.name)
        artworks.delete()
        print(f"   - {Artwork.objects.count()} 개 삭제 완료")
        
        print("\n3. 전시 데이터 삭제...")
        exhibitions = Exhibition.objects.all()
        for exhibition in exhibitions:
            if exhibition.poster_image and default_storage.exists(exhibition.poster_image.name):
                default_storage.delete(exhibition.poster_image.name)
        exhibitions.delete()
        print(f"   - {Exhibition.objects.count()} 개 삭제 완료")
        
        print("\n4. 작가 데이터 삭제...")
        artists = Artist.objects.all()
        for artist in artists:
            if artist.profile_image and default_storage.exists(artist.profile_image.name):
                default_storage.delete(artist.profile_image.name)
        artists.delete()
        print(f"   - {Artist.objects.count()} 개 삭제 완료")
        
        # 5. PostgreSQL 시퀀스 리셋
        print("\n5. 데이터베이스 시퀀스 리셋...")
        with connection.cursor() as cursor:
            # 테이블명 조회
            cursor.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public' 
                AND tablename LIKE 'gallery_%'
            """)
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                # 시퀀스 이름 추정 (Django 기본 패턴)
                sequence_name = f"{table_name}_id_seq"
                
                try:
                    # 시퀀스 리셋
                    cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1")
                    print(f"   - {sequence_name} 리셋 완료")
                except Exception as e:
                    # 시퀀스가 없을 수도 있음
                    pass
        
        # 6. 미디어 폴더 정리
        print("\n6. 미디어 폴더 정리...")
        media_dirs = [
            'media/artists',
            'media/exhibitions',
            'media/artworks',
        ]
        for dir_path in media_dirs:
            full_path = os.path.join('/home/hyuni/hanaart/src', dir_path)
            if os.path.exists(full_path):
                shutil.rmtree(full_path)
                os.makedirs(full_path, exist_ok=True)
                print(f"   - {dir_path} 정리 완료")
        
        print("\n" + "=" * 60)
        print("✅ 갤러리 데이터 초기화가 완료되었습니다!")
        print("=" * 60)
        
        # 현재 상태 확인
        User = get_user_model()
        print("\n현재 데이터베이스 상태:")
        print(f"  - 사용자: {User.objects.count()} 명")
        print(f"  - 작가: {Artist.objects.count()} 명")
        print(f"  - 전시: {Exhibition.objects.count()} 개")
        print(f"  - 작품: {Artwork.objects.count()} 개")
        
    except Exception as e:
        print(f"\n❌ 오류가 발생했습니다: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reset_gallery_data()