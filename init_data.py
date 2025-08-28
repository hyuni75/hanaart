import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.navigator.models import MenuItem

# 메뉴 데이터
menu_data = [
    {'title': '소개·인사말', 'slug': 'about', 'order': 1},
    {'title': '연혁', 'slug': 'history', 'order': 2},
    {'title': '현재전시', 'slug': 'current', 'order': 3},
    {'title': '아트페어', 'slug': 'artfair', 'order': 4},
    {'title': '전속작가', 'slug': 'artists', 'order': 5},
    {'title': '액자제작', 'slug': 'frame', 'order': 6},
    {'title': '찾아오는 길', 'slug': 'location', 'order': 7},
    {'title': '연락처', 'slug': 'contact', 'order': 8},
]

# 기존 메뉴 삭제
MenuItem.objects.all().delete()

# 새 메뉴 생성
for item in menu_data:
    MenuItem.objects.create(
        title=item['title'],
        slug=item['slug'],
        order=item['order'],
        menu_type='section',
        is_active=True,
        is_visible=True
    )

print("초기 메뉴 데이터가 생성되었습니다.")
print(f"생성된 메뉴: {MenuItem.objects.count()}개")