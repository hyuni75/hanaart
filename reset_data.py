#!/usr/bin/env python
"""데이터 초기화 스크립트 - 개별 또는 전체 초기화 + Auto Increment 리셋"""
import os
import sys
import django

sys.path.append('/home/hyuni/hanaart/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.gallery.models import About, History, ArtFair, Artist, Artwork, Frame, Contact
from django.db import connection

def reset_auto_increment(table_name):
    """Auto Increment 값 리셋"""
    with connection.cursor() as cursor:
        cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1")

def reset_about():
    """인사말 데이터 초기화"""
    print("About (인사말) 초기화 중...")
    About.objects.all().delete()
    reset_auto_increment('gallery_about')
    print("  ✓ About 초기화 완료 (Auto Increment 리셋)")

def reset_history():
    """연혁 데이터 초기화"""
    print("History (연혁) 초기화 중...")
    History.objects.all().delete()
    reset_auto_increment('gallery_history')
    print("  ✓ History 초기화 완료 (Auto Increment 리셋)")

def reset_artfair():
    """아트페어 데이터 초기화"""
    print("ArtFair (아트페어) 초기화 중...")
    ArtFair.objects.all().delete()
    reset_auto_increment('gallery_artfair')
    print("  ✓ ArtFair 초기화 완료 (Auto Increment 리셋)")

def reset_artist():
    """작가 및 작품 데이터 초기화"""
    print("Artist & Artwork (작가/작품) 초기화 중...")
    Artwork.objects.all().delete()
    Artist.objects.all().delete()
    reset_auto_increment('gallery_artwork')
    reset_auto_increment('gallery_artist')
    print("  ✓ Artist & Artwork 초기화 완료 (Auto Increment 리셋)")

def reset_frame():
    """액자 데이터 초기화"""
    print("Frame (액자) 초기화 중...")
    Frame.objects.all().delete()
    reset_auto_increment('gallery_frame')
    print("  ✓ Frame 초기화 완료 (Auto Increment 리셋)")

def reset_contact():
    """연락처 데이터 초기화"""
    print("Contact (연락처) 초기화 중...")
    Contact.objects.all().delete()
    reset_auto_increment('gallery_contact')
    print("  ✓ Contact 초기화 완료 (Auto Increment 리셋)")

def reset_all():
    """전체 데이터 초기화"""
    print("\n" + "=" * 80)
    print("전체 데이터 초기화 시작")
    print("=" * 80 + "\n")

    reset_about()
    reset_history()
    reset_artfair()
    reset_artist()
    reset_frame()
    reset_contact()

    print("\n" + "=" * 80)
    print("전체 데이터 초기화 완료!")
    print("=" * 80)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법:")
        print("  python reset_data.py all          # 전체 초기화")
        print("  python reset_data.py about        # 인사말만 초기화")
        print("  python reset_data.py history      # 연혁만 초기화")
        print("  python reset_data.py artfair      # 아트페어만 초기화")
        print("  python reset_data.py artist       # 작가/작품만 초기화")
        print("  python reset_data.py frame        # 액자만 초기화")
        print("  python reset_data.py contact      # 연락처만 초기화")
        sys.exit(1)

    target = sys.argv[1].lower()

    if target == 'all':
        reset_all()
    elif target == 'about':
        reset_about()
    elif target == 'history':
        reset_history()
    elif target == 'artfair':
        reset_artfair()
    elif target == 'artist':
        reset_artist()
    elif target == 'frame':
        reset_frame()
    elif target == 'contact':
        reset_contact()
    else:
        print(f"❌ 알 수 없는 옵션: {target}")
        print("사용 가능한 옵션: all, about, history, artfair, artist, frame, contact")
        sys.exit(1)
