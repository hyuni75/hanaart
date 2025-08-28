import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.moderation.models import FilterRule, BlockedWord, SpamPattern
from apps.gallery.models import Artist, Exhibition
from datetime import date, datetime
from django.utils import timezone

# 필터링 규칙 추가
filter_rules = [
    {'name': '욕설 필터', 'rule_type': 'word', 'pattern': '시발', 'action': 'replace', 'severity': 9},
    {'name': '비속어 필터', 'rule_type': 'word', 'pattern': '개새끼', 'action': 'replace', 'severity': 9},
    {'name': 'URL 차단', 'rule_type': 'url', 'pattern': 'http', 'action': 'block', 'severity': 7},
    {'name': '전화번호 차단', 'rule_type': 'regex', 'pattern': r'\d{3}-\d{4}-\d{4}', 'action': 'replace', 'severity': 5},
    {'name': '이메일 차단', 'rule_type': 'regex', 'pattern': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 'action': 'replace', 'severity': 5},
]

for rule_data in filter_rules:
    FilterRule.objects.get_or_create(
        name=rule_data['name'],
        defaults=rule_data
    )

# 금지어 추가
blocked_words = [
    {'word': '씨발', 'category': '욕설', 'severity': 10},
    {'word': '존나', 'category': '욕설', 'severity': 8},
    {'word': '닥쳐', 'category': '욕설', 'severity': 7},
    {'word': '카지노', 'category': '광고', 'severity': 8},
    {'word': '대출', 'category': '광고', 'severity': 8},
    {'word': '성인', 'category': '광고', 'severity': 9},
]

for word_data in blocked_words:
    BlockedWord.objects.get_or_create(
        word=word_data['word'],
        defaults=word_data
    )

# 스팸 패턴 추가
spam_patterns = [
    {
        'name': '반복 문자',
        'pattern': r'(.)\1{5,}',
        'description': '같은 문자가 6번 이상 반복',
        'is_regex': True
    },
    {
        'name': '과도한 특수문자',
        'pattern': r'[!@#$%^&*]{5,}',
        'description': '특수문자가 5개 이상 연속',
        'is_regex': True
    },
    {
        'name': '광고 키워드',
        'pattern': '클릭하세요',
        'description': '광고성 문구',
        'is_regex': False
    },
]

for pattern_data in spam_patterns:
    SpamPattern.objects.get_or_create(
        name=pattern_data['name'],
        defaults=pattern_data
    )

# 샘플 작가 데이터 추가
artists_data = [
    {
        'name': '김정숙',
        'name_en': 'Kim Jung-Sook',
        'bio': '추계예대 서양화과 졸업. 국내외 개인전 24회, 해외/국내 아트페어 및 단체전 300여 회 참여.',
        'is_exclusive': True,
        'display_order': 1
    },
    {
        'name': '이한',
        'name_en': 'Lee Han',
        'bio': '옻칠의 물성과 반복적 붓질을 결합해 빛·몸·시간이 어우러지는 장(field)을 구축.',
        'is_exclusive': True,
        'display_order': 2
    },
    {
        'name': '박세연',
        'name_en': 'Park Se-Yeon',
        'bio': '건국대 금속공예 전공. 2024–25 국내 다수 개인전 및 서울·홍콩·싱가포르 등 아트페어 참가.',
        'is_exclusive': True,
        'display_order': 3
    },
    {
        'name': '김점선',
        'name_en': 'Kim Jeom-Sun',
        'bio': '자유분방한 선과 색으로 한국적 감수성을 현대적으로 풀어낸 작가.',
        'is_exclusive': True,
        'display_order': 4
    },
    {
        'name': '이호철',
        'name_en': 'Lee Ho-Cheol',
        'bio': '1958년 서울 출생. 홍익대 서양화과 및 동대학원. 국내외 전시 150여 회 참여.',
        'is_exclusive': True,
        'display_order': 5
    },
    {
        'name': '하금숙',
        'name_en': 'Ha Geum-Sook',
        'bio': '1995–2010 개인전 12회 등. 꽃·잎의 리듬을 투명한 색층으로 구현.',
        'is_exclusive': True,
        'display_order': 6
    },
]

for artist_data in artists_data:
    Artist.objects.get_or_create(
        name=artist_data['name'],
        defaults=artist_data
    )

# 현재 전시 추가
exhibition_data = {
    'title': '이한 초대전',
    'title_en': 'Rhythm of Light',
    'slug': 'lee-han-2025',
    'exhibition_type': 'solo',
    'description': '반복 제스처와 옻칠의 물성으로 빛의 리듬을 시각화하는 이한 작가의 신작을 선보입니다.',
    'start_date': date(2025, 1, 20),
    'end_date': date(2025, 2, 2),
    'is_current': True,
    'is_featured': True,
}

exhibition, created = Exhibition.objects.get_or_create(
    slug=exhibition_data['slug'],
    defaults=exhibition_data
)

if created:
    # 작가 연결
    lee_han = Artist.objects.get(name='이한')
    exhibition.artists.add(lee_han)
    print("전시 데이터가 추가되었습니다.")

print("\n초기 데이터 설정이 완료되었습니다.")
print(f"필터 규칙: {FilterRule.objects.count()}개")
print(f"금지어: {BlockedWord.objects.count()}개")
print(f"스팸 패턴: {SpamPattern.objects.count()}개")
print(f"작가: {Artist.objects.count()}명")
print(f"전시: {Exhibition.objects.count()}개")