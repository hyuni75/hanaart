from django.db import models
from apps.core.models import TimeStampedModel

class MenuItem(TimeStampedModel):
    """네비게이션 메뉴 아이템"""
    MENU_TYPES = [
        ('page', '페이지 링크'),
        ('external', '외부 링크'),
        ('section', '섹션 앵커'),
    ]
    
    title = models.CharField(max_length=100, verbose_name='메뉴 제목')
    slug = models.SlugField(unique=True, verbose_name='슬러그')
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='children',
        verbose_name='상위 메뉴'
    )
    menu_type = models.CharField(max_length=20, choices=MENU_TYPES, default='page', verbose_name='메뉴 타입')
    url = models.CharField(max_length=200, blank=True, verbose_name='URL')
    icon = models.CharField(max_length=50, blank=True, verbose_name='아이콘 클래스')
    order = models.IntegerField(default=0, verbose_name='정렬 순서')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    is_visible = models.BooleanField(default=True, verbose_name='표시 여부')
    target_blank = models.BooleanField(default=False, verbose_name='새창 열기')
    
    # SEO 필드
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='메타 제목')
    meta_description = models.TextField(blank=True, verbose_name='메타 설명')
    
    class Meta:
        verbose_name = '메뉴 아이템'
        verbose_name_plural = '메뉴 아이템 목록'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        if self.menu_type == 'external':
            return self.url
        elif self.menu_type == 'section':
            return f'#{self.slug}'
        else:
            return f'/{self.slug}/'