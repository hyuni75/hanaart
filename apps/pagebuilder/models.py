from django.db import models
from apps.core.models import TimeStampedModel
import json

class Template(TimeStampedModel):
    """페이지 템플릿"""
    TEMPLATE_TYPES = [
        ('single', '단일 컬럼'),
        ('two-column', '2컬럼'),
        ('three-column', '3컬럼'),
        ('hero', '히어로 페이지'),
        ('gallery', '갤러리'),
        ('custom', '커스텀'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='템플릿 이름')
    slug = models.SlugField(unique=True, verbose_name='슬러그')
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES, default='single', verbose_name='템플릿 타입')
    description = models.TextField(blank=True, verbose_name='설명')
    html_template = models.TextField(blank=True, verbose_name='HTML 템플릿')
    css_styles = models.TextField(blank=True, verbose_name='CSS 스타일')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    
    class Meta:
        verbose_name = '템플릿'
        verbose_name_plural = '템플릿 목록'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Page(TimeStampedModel):
    """동적 페이지"""
    title = models.CharField(max_length=200, verbose_name='제목')
    slug = models.SlugField(unique=True, verbose_name='슬러그')
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='템플릿')
    is_published = models.BooleanField(default=False, verbose_name='게시 여부')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='게시일')
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='메타 제목')
    meta_description = models.TextField(blank=True, verbose_name='메타 설명')
    meta_keywords = models.CharField(max_length=500, blank=True, verbose_name='메타 키워드')
    
    # 상호작용 설정
    enable_comments = models.BooleanField(default=True, verbose_name='댓글 허용')
    enable_likes = models.BooleanField(default=True, verbose_name='좋아요 허용')
    
    class Meta:
        verbose_name = '페이지'
        verbose_name_plural = '페이지 목록'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/{self.slug}/'

class Block(TimeStampedModel):
    """페이지 블록"""
    BLOCK_TYPES = [
        ('text', '텍스트'),
        ('image', '이미지'),
        ('gallery', '갤러리'),
        ('video', '비디오'),
        ('html', 'HTML'),
        ('map', '지도'),
        ('contact', '연락처'),
        ('spacer', '여백'),
    ]
    
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='blocks', verbose_name='페이지')
    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES, verbose_name='블록 타입')
    title = models.CharField(max_length=200, blank=True, verbose_name='제목')
    content = models.TextField(blank=True, verbose_name='내용')
    
    # JSON 필드로 다양한 설정 저장
    settings_json = models.TextField(default='{}', verbose_name='설정')
    
    # 정렬 및 레이아웃
    order = models.IntegerField(default=0, verbose_name='정렬 순서')
    css_class = models.CharField(max_length=100, blank=True, verbose_name='CSS 클래스')
    
    is_visible = models.BooleanField(default=True, verbose_name='표시 여부')
    
    class Meta:
        verbose_name = '블록'
        verbose_name_plural = '블록 목록'
        ordering = ['page', 'order']
    
    def __str__(self):
        return f'{self.page.title} - {self.get_block_type_display()}'
    
    @property
    def settings(self):
        try:
            return json.loads(self.settings_json)
        except:
            return {}
    
    @settings.setter
    def settings(self, value):
        self.settings_json = json.dumps(value, ensure_ascii=False)

class Media(TimeStampedModel):
    """미디어 파일"""
    MEDIA_TYPES = [
        ('image', '이미지'),
        ('video', '비디오'),
        ('document', '문서'),
        ('other', '기타'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='이름')
    file = models.FileField(upload_to='media/%Y/%m/', verbose_name='파일')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, default='image', verbose_name='미디어 타입')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='대체 텍스트')
    caption = models.TextField(blank=True, verbose_name='캡션')
    
    # 메타데이터
    file_size = models.IntegerField(default=0, verbose_name='파일 크기')
    width = models.IntegerField(null=True, blank=True, verbose_name='너비')
    height = models.IntegerField(null=True, blank=True, verbose_name='높이')
    
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, verbose_name='업로더')
    
    class Meta:
        verbose_name = '미디어'
        verbose_name_plural = '미디어 목록'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name