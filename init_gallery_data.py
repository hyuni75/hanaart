import os
import django
from datetime import date, datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.gallery.models import Artist, Exhibition, Artwork

def create_initial_data():
    """갤러리 초기 데이터 생성"""
    
    print("갤러리 초기 데이터 생성 시작...")
    
    # 1. 작가 데이터 생성
    artists_data = [
        {
            'name': '하금숙',
            'name_en': 'Ha Geum Sook',
            'birth_year': 1965,
            'bio': '한국 전통 회화를 현대적으로 재해석하는 작가로, 자연과 인간의 조화를 주제로 작업합니다.',
            'education': '서울대학교 미술대학 동양화과 졸업\n서울대학교 대학원 동양화과 석사',
            'awards': '2020 대한민국 미술대전 대상\n2018 서울미술상 수상',
            'is_exclusive': True,
            'is_active': True,
            'display_order': 1
        },
        {
            'name': '이한',
            'name_en': 'Lee Han',
            'birth_year': 1972,
            'bio': '도시 풍경과 현대인의 삶을 독특한 색채로 표현하는 작가입니다.',
            'education': '홍익대학교 미술대학 회화과 졸업\n파리 국립미술학교 수학',
            'awards': '2019 이중섭 미술상\n2017 하종현 미술상',
            'is_exclusive': True,
            'is_active': True,
            'display_order': 2
        },
        {
            'name': '김점선',
            'name_en': 'Kim Jeom Sun',
            'birth_year': 1968,
            'bio': '추상과 구상의 경계를 넘나들며 독창적인 조형언어를 구축하는 작가입니다.',
            'education': '이화여자대학교 조형예술대학 졸업\n뉴욕 프랫 인스티튜트 MFA',
            'awards': '2021 광주비엔날레 특별상\n2020 부산비엔날레 우수상',
            'is_exclusive': True,
            'is_active': True,
            'display_order': 3
        },
        {
            'name': '김종성',
            'name_en': 'Kim Jong Sung',
            'birth_year': 1975,
            'bio': '자연의 순환과 생명력을 캔버스에 담아내는 작가입니다.',
            'education': '중앙대학교 예술대학 한국화과 졸업',
            'awards': '2018 청년작가상',
            'is_exclusive': True,
            'is_active': True,
            'display_order': 4
        },
        {
            'name': '이호',
            'name_en': 'Lee Ho',
            'birth_year': 1980,
            'bio': '미니멀리즘과 한국적 정서를 결합한 독특한 작품세계를 구축합니다.',
            'education': '한국예술종합학교 조형예술과 졸업',
            'awards': '2019 송은미술대상',
            'is_exclusive': True,
            'is_active': True,
            'display_order': 5
        },
        {
            'name': '박신영',
            'name_en': 'Park Shin Young',
            'birth_year': 1978,
            'bio': '일상의 사물들을 새로운 시각으로 재해석하는 설치미술가입니다.',
            'education': '계원예술대학교 졸업',
            'awards': '2020 올해의 청년작가상',
            'is_exclusive': True,
            'is_active': True,
            'display_order': 6
        }
    ]
    
    # 기존 데이터 삭제 (선택적)
    print("기존 데이터 삭제 중...")
    Artist.objects.all().delete()
    Exhibition.objects.all().delete()
    Artwork.objects.all().delete()
    
    # 작가 생성
    artists = []
    for data in artists_data:
        artist = Artist.objects.create(**data)
        artists.append(artist)
        print(f"작가 생성: {artist.name}")
    
    # 2. 전시 데이터 생성
    today = timezone.now().date()
    
    exhibition = Exhibition.objects.create(
        title='The Journey',
        title_en='The Journey',
        slug='the-journey-2025',
        exhibition_type='group',
        description='여섯 작가의 예술적 여정을 담은 특별전시입니다. 각자의 독특한 시각과 기법으로 표현한 현대미술의 다양성을 만나보실 수 있습니다.',
        start_date=today - timedelta(days=7),
        end_date=today + timedelta(days=30),
        opening_date=timezone.now() - timedelta(days=7),
        venue='하나아트갤러리',
        venue_address='서울특별시 종로구 인사동10길 2, 단성빌딩 2층',
        is_current=True,
        is_featured=True,
        is_published=True,
        meta_description='하나아트갤러리 2025년 기획전시 The Journey'
    )
    
    # 전시에 작가 연결
    exhibition.artists.set(artists)
    print(f"전시 생성: {exhibition.title}")
    
    # 3. 작품 데이터 생성
    artworks_data = [
        # 하금숙 작품
        {
            'artist': artists[0],
            'title': '봄의 정원',
            'title_en': 'Spring Garden',
            'artwork_type': 'painting',
            'year': 2024,
            'medium': '한지에 수묵채색',
            'size': '130 x 162 cm',
            'description': '봄의 생명력을 한국 전통 기법으로 표현한 작품',
            'price': 15000000,
            'is_for_sale': True,
            'is_featured': True,
            'display_order': 1
        },
        {
            'artist': artists[0],
            'title': '바람의 노래',
            'title_en': 'Song of Wind',
            'artwork_type': 'painting',
            'year': 2024,
            'medium': '한지에 수묵',
            'size': '100 x 100 cm',
            'description': '바람에 흔들리는 대나무를 통해 유연함과 강인함을 동시에 표현',
            'price': 8000000,
            'is_for_sale': True,
            'display_order': 2
        },
        # 이한 작품
        {
            'artist': artists[1],
            'title': '도시의 밤',
            'title_en': 'Urban Night',
            'artwork_type': 'painting',
            'year': 2024,
            'medium': '캔버스에 유채',
            'size': '145.5 x 112 cm',
            'description': '현대 도시의 야경을 독특한 색채로 표현',
            'price': 12000000,
            'is_for_sale': True,
            'is_featured': True,
            'display_order': 3
        },
        # 김점선 작품
        {
            'artist': artists[2],
            'title': '경계의 시간',
            'title_en': 'Time of Boundary',
            'artwork_type': 'painting',
            'year': 2024,
            'medium': '캔버스에 아크릴',
            'size': '130 x 130 cm',
            'description': '추상과 구상의 경계를 탐구한 실험적 작품',
            'price': 10000000,
            'is_for_sale': True,
            'display_order': 4
        },
        # 김종성 작품
        {
            'artist': artists[3],
            'title': '생명의 순환',
            'title_en': 'Cycle of Life',
            'artwork_type': 'painting',
            'year': 2024,
            'medium': '한지에 채색',
            'size': '90 x 120 cm',
            'description': '자연의 순환과 재생을 표현한 작품',
            'price': 7000000,
            'is_for_sale': True,
            'display_order': 5
        },
        # 이호 작품
        {
            'artist': artists[4],
            'title': '정적',
            'title_en': 'Silence',
            'artwork_type': 'painting',
            'year': 2024,
            'medium': '캔버스에 유채',
            'size': '100 x 100 cm',
            'description': '미니멀한 구성으로 고요함을 표현',
            'price': 9000000,
            'is_for_sale': True,
            'display_order': 6
        }
    ]
    
    # 작품 생성 및 전시 연결
    for data in artworks_data:
        artwork = Artwork.objects.create(
            artist=data['artist'],
            title=data['title'],
            title_en=data.get('title_en', ''),
            artwork_type=data.get('artwork_type', 'painting'),
            year=data.get('year'),
            medium=data.get('medium', ''),
            size=data.get('size', ''),
            description=data.get('description', ''),
            price=data.get('price'),
            is_for_sale=data.get('is_for_sale', True),
            is_featured=data.get('is_featured', False),
            is_published=True,
            display_order=data.get('display_order', 0)
        )
        artwork.exhibitions.add(exhibition)
        print(f"작품 생성: {artwork.title} - {artwork.artist.name}")
    
    print("\n=== 갤러리 초기 데이터 생성 완료 ===")
    print(f"생성된 작가: {Artist.objects.count()}명")
    print(f"생성된 전시: {Exhibition.objects.count()}개")
    print(f"생성된 작품: {Artwork.objects.count()}점")
    
    return True

if __name__ == '__main__':
    create_initial_data()