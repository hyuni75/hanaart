#!/usr/bin/env python
"""
초기 전속작가 데이터를 로드하는 스크립트
"""
import os
import sys
import django

# Django 설정 초기화
sys.path.insert(0, '/home/hyuni/hanaart/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.gallery.models import SimpleArtist
from django.core.files import File
from django.core.files.base import ContentFile
import shutil

def load_initial_artists():
    """초기 작가 데이터 로드"""
    
    # 기존 데이터 삭제 (필요시)
    # SimpleArtist.objects.all().delete()
    
    artists_data = [
        {
            'name': '김정숙',
            'bio': '추계예대 서양화과 졸업. 국내외 개인전 24회, 해외/국내 아트페어 및 단체전 300여 회 참여.',
            'display_order': 1,
            'images': ['kimjs_01.jpg', 'kimjs_02.jpg', 'kimjs_03.jpg']
        },
        {
            'name': '김점선',
            'bio': '자유분방한 선과 색으로 한국적 감수성을 현대적으로 풀어낸 작가. 말·오리 등 상징적 모티프의 회화로 사랑받음.',
            'display_order': 2,
            'images': ['kimjeomsun_01.jpg', 'kimjeomsun_02.jpg', 'kimjeomsun_03.jpg']
        },
        {
            'name': '박세연',
            'bio': '건국대 금속공예 전공. 2024–25 국내 다수 개인전 및 서울·홍콩·싱가포르 등 아트페어 참가.',
            'display_order': 3,
            'images': ['parksy_01.jpg', 'parksy_02.jpg', 'parksy_03.jpg']
        },
        {
            'name': '이한',
            'bio': '옻칠의 물성과 반복적 붓질을 결합해 빛·몸·시간이 어우러지는 장(field)을 구축.',
            'display_order': 4,
            'images': ['ihan_a.jpg', 'ihan_b.jpg', 'ihan_c.jpg']
        },
        {
            'name': '이호철',
            'bio': '1958년 서울 출생. 홍익대 서양화과 및 동대학원. 국내외 전시 150여 회 참여.',
            'display_order': 5,
            'images': ['leeho_01.jpg', 'leeho_02.jpg', 'leeho_03.jpg']
        },
        {
            'name': '하금숙',
            'bio': '1995–2010 개인전 12회 등. 꽃·잎의 리듬을 투명한 색층으로 구현.',
            'display_order': 6,
            'images': ['hagumsuk_01.jpg', 'hagumsuk_02.jpg', 'hagumsuk_03.jpg']
        }
    ]
    
    static_img_path = '/home/hyuni/hanaart/src/static/img/'
    
    for artist_data in artists_data:
        # 이미 존재하는지 확인
        if SimpleArtist.objects.filter(name=artist_data['name']).exists():
            print(f"작가 {artist_data['name']}은(는) 이미 존재합니다. 건너뜁니다.")
            continue
            
        try:
            artist = SimpleArtist(
                name=artist_data['name'],
                bio=artist_data['bio'],
                display_order=artist_data['display_order'],
                is_active=True
            )
            
            # 이미지 파일 처리
            images = artist_data['images']
            
            # 첫 번째 이미지 (필수)
            if images[0]:
                img_path = os.path.join(static_img_path, images[0])
                if os.path.exists(img_path):
                    with open(img_path, 'rb') as f:
                        artist.artwork1.save(images[0], File(f), save=False)
            
            # 두 번째 이미지 (선택)
            if len(images) > 1 and images[1]:
                img_path = os.path.join(static_img_path, images[1])
                if os.path.exists(img_path):
                    with open(img_path, 'rb') as f:
                        artist.artwork2.save(images[1], File(f), save=False)
            
            # 세 번째 이미지 (선택)
            if len(images) > 2 and images[2]:
                img_path = os.path.join(static_img_path, images[2])
                if os.path.exists(img_path):
                    with open(img_path, 'rb') as f:
                        artist.artwork3.save(images[2], File(f), save=False)
            
            artist.save()
            print(f"작가 {artist_data['name']} 추가 완료")
            
        except Exception as e:
            print(f"작가 {artist_data['name']} 추가 중 오류 발생: {e}")
    
    print("\n초기 작가 데이터 로드 완료!")
    total = SimpleArtist.objects.filter(is_active=True).count()
    print(f"활성화된 전속작가 총 {total}명")

if __name__ == '__main__':
    load_initial_artists()