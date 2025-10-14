#!/usr/bin/env python
"""전체 데이터 통합 등록 스크립트 - static → media 복사"""
import os
import sys
import django
import shutil

sys.path.append('/home/hyuni/hanaart/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.gallery.models import About, History, ArtFair, Artist, Artwork, Frame, Contact
from django.core.files import File
from django.conf import settings
import glob

print("=" * 80)
print("전체 데이터 통합 등록 (static → media 복사)")
print("=" * 80)

# ==================== 1. About (인사말) ====================
print("\n[1/6] About (인사말) 데이터 등록...")
About.objects.all().delete()

about_data = {
    'title': '인사말',
    'content_1': '하나아트갤러리는 1990년 오픈하여 한국화랑협회 회원화랑으로 작가와 관람객이 예술로 교감하고 국내외 유망 신진작가를 발굴하고 중견, 원로작가까지 폭넓은 스펙트럼을 아우르며 회화, 조각, 설치, 전통미술 등 다양한 장르를 기획, 전시합니다.',
    'content_2': '또한 각종 국내, 외 아트페어와 해외교류전을 통해 한국미술의 가치를 널리 알리고 하나액자를 운영하여 작품보존과 미학적 완성도를 높이고 있다.',
    'content_3': '앞으로 예술과 삶을 잇는 다리로서 관람객에게 영감을 전하는 전시를 지속적으로 선보이겠습니다.',
    'is_active': True
}

about = About.objects.create(**about_data)

# static 이미지를 media로 복사
intro_bg = './static/images/intro_bg.jpg'
intro_cad = './static/images/intro_cad.jpg'

if os.path.exists(intro_bg):
    with open(intro_bg, 'rb') as f:
        about.image_1.save('intro_bg.jpg', File(f), save=True)
    print(f"  ✓ 전시장 내부 이미지 등록 (static → media)")

if os.path.exists(intro_cad):
    with open(intro_cad, 'rb') as f:
        about.image_2.save('intro_cad.jpg', File(f), save=True)
    print(f"  ✓ 전시장 도면 이미지 등록 (static → media)")

print(f"  ✓ About 데이터 등록 완료")

# ==================== 2. History (연혁) ====================
print("\n[2/6] History (연혁) 데이터 등록...")
History.objects.all().delete()

histories = [
    (1990, "하나화랑 오픈", 1),
    (2001, """한국화랑협회 회원가입
한국판화미술진흥회 회원가입
서울판화미술제 참가 (오세영, 이두식, 이석주)""", 2),
    (2003, """강원랜드 아트윅 150여점 판화 납품
한국국제아트페어(KIAF) 참가""", 3),
    (2004, """한국국제아트페어(KIAF) 참가 (김점선, 정강자)
현대미술진흥원 판화 400여점 납품""", 4),
    (2005, """한국국제아트페어(KIAF) 참가 (김점선, 장혜용)
중부푸드뱅크, 남서울대학교 지식정보관 각 100여점 납품""", 5),
    (2006, """김점선 작가 문화상품 브랜드 "점선스타일" 런칭
아도니스 호텔 200여점 납품
한국국제아트페어(KIAF) 참가 (김점선, 이순형)
블랙밸리 클럽하우스 예술장식품 제작ㆍ설치
강원랜드 아트웍 1000여점 판화 납품""", 6),
    (2007, "법남서울대 평생교육원 납품 및 설치", 7),
    (2008, """법인사업자 설립 "주식회사 인사하나아트"
리빙디자인아트페어 참가
한국국제아트페어(KIAF) 참가 (정현숙)
서울국제판화사진아트페어(SIPA) 참가 (임종만, 고혜련)
열린미술시장(SOAF) 참가 (김점선 외)""", 8),
    (2010, """한국국제아트페어(KIAF) 참가 (김점선, 김정숙, 정강자)
인사미술제(INSAF) 참가""", 9),
    (2011, """한국국제아트페어(KIAF) 참가 (김점선, 김정숙, 하금숙)
남서울대학교 엘림관 납품 및 설치""", 10),
    (2012, """인사미술제(INSAF) 참가
한국국제아트페어(KIAF) 참가 (김점선, 조영남)""", 11),
    (2013, "리빙 아트페어 참가", 12),
    (2022, """대구 아트페어 참가
아트 광주 페어 참가""", 13),
    (2023, """한국국제아트페어(KIAF) 참가
화랑미술제 참가
제주 아트페어 참가
인천 아트 쇼 참가""", 14),
]

for year, content, order in histories:
    History.objects.create(year=year, content=content, order=order, is_active=True)

print(f"  ✓ 총 {len(histories)}개 연혁 등록 완료")

# ==================== 3. ArtFair (아트페어) ====================
print("\n[3/6] ArtFair (아트페어) 데이터 등록...")
ArtFair.objects.all().delete()

artfairs = [
    {'year': 2009, 'title': '한국국제아트페어(KIAF)', 'description': '한국국제아트페어 2009 참가', 'image': '2009_한국국제아트페어.png'},
    {'year': 2010, 'title': '한국국제아트페어(KIAF)', 'description': '한국국제아트페어 2010 참가', 'image': '2010_한국국제아트페어.png'},
    {'year': 2011, 'title': '한국국제아트페어(KIAF)', 'description': '한국국제아트페어 2011 참가', 'image': '2011_한국국제아트페어.png'},
    {'year': 2013, 'title': '한국국제아트페어(KIAF)', 'description': '한국국제아트페어 2013 참가', 'image': '2013_한국국제아트페어.png'},
    {'year': 2014, 'title': '화랑미술제', 'description': '화랑미술제 2014 참가', 'image': '2014_화랑미술제.png'},
    {'year': 2015, 'title': '한국국제아트페어(KIAF)', 'description': '한국국제아트페어 2015 참가', 'image': '2015_한국국제아트페어.png'},
    {'year': 2017, 'title': '한국국제아트페어(KIAF)', 'description': '한국국제아트페어 2017 참가', 'image': '2017_한국국제아트페어.png'},
    {'year': 2023, 'title': '한국국제아트페어(KIAF)', 'description': '한국국제아트페어 2023 참가', 'image': '2023_한국국제아트페어.png'},
]

for data in artfairs:
    artfair = ArtFair.objects.create(
        year=data['year'],
        title=data['title'],
        description=data['description'],
        is_active=True
    )
    # static 이미지를 media로 복사
    src_path = f'./static/images/{data["image"]}'
    if os.path.exists(src_path):
        with open(src_path, 'rb') as f:
            artfair.image.save(data['image'], File(f), save=True)

print(f"  ✓ 총 {len(artfairs)}개 아트페어 등록 완료 (static → media)")

# ==================== 4. Artist & Artwork ====================
print("\n[4/6] Artist & Artwork 데이터 등록...")
Artist.objects.all().delete()
Artwork.objects.all().delete()

artists_data = [
    {'name': '김정숙', 'name_en': 'Kim Jung-sook', 'description': '추계예대 서양화과 졸업. 국내외 개인전 24회, 해외/국내 아트페어 및 단체전 300여 회 참여.', 'order': 1},
    {'name': '김점선', 'name_en': 'Kim Jeom-sun', 'description': '자유분방한 선과 색으로 한국적 감수성을 현대적으로 풀어낸 작가. 말·오리 등 상징적 모티프의 회화로 사랑받음.', 'order': 2},
    {'name': '박세연', 'name_en': 'Park Se-yeon', 'description': '건국대 금속공예 전공. 2024–25 국내 다수 개인전 및 서울·홍콩·싱가포르 등 아트페어 참가.', 'order': 3},
    {'name': '이한', 'name_en': 'Lee Han', 'description': '옻칠의 물성과 반복적 붓질을 결합해 빛·몸·시간이 어우러지는 장(field)을 구축.', 'order': 4},
    {'name': '하금숙', 'name_en': 'Ha Geum-sook', 'description': '1995–2010 개인전 12회 등. 꽃·잎의 리듬을 투명한 색층으로 구현.', 'order': 5}
]

artists_created = {}
for artist_data in artists_data:
    artist = Artist.objects.create(**artist_data)
    artists_created[artist.name] = artist

print(f"  ✓ 총 {len(artists_data)}명 작가 등록 완료")

# 작가별 작품 등록 (static → media 복사)
artist_folders = {
    '김정숙': 'kimjungsook',
    '김점선': 'kimjeomsun',
    '박세연': 'parseyeon',
    '이한': 'leehan',
    '하금숙': 'hagumsuk'
}

total_artworks = 0
for artist_name, folder_name in artist_folders.items():
    artist = artists_created[artist_name]
    folder_path = f'./static/images/{folder_name}'

    if not os.path.exists(folder_path):
        continue

    image_files = []
    for ext in ['*.jpg', '*.JPG', '*.jpeg', '*.JPEG']:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))

    image_files = [f for f in image_files if not f.endswith('Zone.Identifier')]
    image_files.sort()

    for idx, image_path in enumerate(image_files, 1):
        file_name = os.path.basename(image_path)

        artwork = Artwork.objects.create(
            artist=artist,
            title=f'{artist_name} 작품 {idx}',
            description='',
            order=idx,
            is_active=True,
            is_featured=(idx == 1 and artist_name in ['김점선', '하금숙'])
        )

        # static에서 media로 복사
        with open(image_path, 'rb') as f:
            artwork.image.save(file_name, File(f), save=True)

        total_artworks += 1

print(f"  ✓ 총 {total_artworks}개 작품 등록 완료 (static → media)")

# ==================== 5. Frame (액자) ====================
print("\n[5/6] Frame (액자) 데이터 등록...")
Frame.objects.all().delete()

frame_desc = "'하나액자'는 작품의 가치를 더욱 빛나게 하는 맞춤형 프레임을 제작합니다. 30년 전통과 현대적 감각을 담아 현대 공간에 어울리는 최적의 액자를 제안합니다."

# Frame 모델은 1개 항목에 3개 이미지(image_1, image_2, image_3)
frame = Frame.objects.create(
    title='액자 제작',
    description=frame_desc,
    order=1,
    is_active=True
)

# 3개 이미지 등록
for i in range(1, 4):
    src_path = f'./static/images/frame{i}.png'
    if os.path.exists(src_path):
        with open(src_path, 'rb') as f:
            if i == 1:
                frame.image_1.save(f'frame{i}.png', File(f), save=True)
            elif i == 2:
                frame.image_2.save(f'frame{i}.png', File(f), save=True)
            elif i == 3:
                frame.image_3.save(f'frame{i}.png', File(f), save=True)

print(f"  ✓ 액자 1개 항목에 3개 이미지 등록 완료 (static → media)")

# ==================== 6. Contact (연락처) ====================
print("\n[6/6] Contact (연락처) 데이터 등록...")
Contact.objects.all().delete()

contact = Contact.objects.create(
    title='하나아트갤러리 본점(인사동)',
    ceo_name='이방은',
    ceo_name_en='Lee, Bang-Eun',
    phone='02-736-7877',
    fax='02-736-4877',
    mobile='010-8681-7277',
    email='hanaartag@naver.com',
    address='서울특별시 종로구 인사동10길 2, 단성빌딩 2층(갤러리) / 3층(액자)',
    address_en='2, Insadong 10-gil, Jongno-gu, Seoul, Republic of Korea',
    is_active=True
)

print(f"  ✓ 연락처 정보 등록 완료")

print("\n" + "=" * 80)
print("전체 데이터 통합 등록 완료!")
print("=" * 80)
print(f"About: 1개")
print(f"History: {len(histories)}개")
print(f"ArtFair: {len(artfairs)}개")
print(f"Artist: {len(artists_data)}명")
print(f"Artwork: {total_artworks}개")
print(f"Frame: 3개")
print(f"Contact: 1개")
print("=" * 80)
print("※ 모든 이미지가 static → media 폴더로 복사되었습니다.")
print("=" * 80)
