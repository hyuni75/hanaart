from django.db import models
from apps.core.models import TimeStampedModel
from .utils import ImageOptimizer
import os

class Artist(TimeStampedModel):
    """작가 모델"""
    name = models.CharField(max_length=100, verbose_name='작가명')
    name_en = models.CharField(max_length=100, blank=True, verbose_name='영문명')
    birth_year = models.IntegerField(null=True, blank=True, verbose_name='출생년도')
    
    profile_image = models.ImageField(upload_to='artists/profiles/', blank=True, null=True, verbose_name='프로필 이미지')
    bio = models.TextField(blank=True, verbose_name='약력')
    education = models.TextField(blank=True, verbose_name='학력')
    awards = models.TextField(blank=True, verbose_name='수상경력')
    
    # 연락처
    email = models.EmailField(blank=True, verbose_name='이메일')
    phone = models.CharField(max_length=20, blank=True, verbose_name='전화번호')
    website = models.URLField(blank=True, verbose_name='웹사이트')
    instagram = models.CharField(max_length=100, blank=True, verbose_name='인스타그램')
    
    # 상태
    is_exclusive = models.BooleanField(default=False, verbose_name='전속작가')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    display_order = models.IntegerField(default=0, verbose_name='표시 순서')
    
    class Meta:
        verbose_name = '작가'
        verbose_name_plural = '작가 목록'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # 프로필 이미지 최적화 - 삭제 작업 시에는 이미지 처리 건너뛰기
        if self.profile_image and not kwargs.get('force_insert', False):
            try:
                # 이미지가 변경되었는지 확인
                if self.pk:
                    try:
                        old_instance = Artist.objects.get(pk=self.pk)
                        if old_instance.profile_image != self.profile_image and hasattr(self.profile_image, 'file'):
                            # 이미지 최적화 (최대 800x800)
                            self.profile_image = ImageOptimizer.create_medium(self.profile_image)
                    except Artist.DoesNotExist:
                        pass
                elif hasattr(self.profile_image, 'file'):
                    # 새 객체인 경우
                    self.profile_image = ImageOptimizer.create_medium(self.profile_image)
            except Exception as e:
                # 이미지 처리 실패 시 원본 유지
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"이미지 최적화 실패: {e}")
        
        super().save(*args, **kwargs)

class Exhibition(TimeStampedModel):
    """전시 모델"""
    EXHIBITION_TYPES = [
        ('solo', '개인전'),
        ('group', '단체전'),
        ('special', '특별전'),
        ('fair', '아트페어'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='전시명')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='영문 전시명')
    exhibition_type = models.CharField(max_length=20, choices=EXHIBITION_TYPES, default='solo', verbose_name='전시 유형')
    
    artists = models.ManyToManyField(Artist, related_name='exhibitions', verbose_name='참여 작가')
    
    # 전시 정보
    description = models.TextField(blank=True, verbose_name='전시 설명')
    poster_image = models.ImageField(upload_to='exhibitions/posters/', blank=True, null=True, verbose_name='포스터 이미지')
    
    # 일정
    start_date = models.DateField(verbose_name='시작일')
    end_date = models.DateField(verbose_name='종료일')
    opening_date = models.DateTimeField(null=True, blank=True, verbose_name='오프닝 일시')
    
    # 장소
    venue = models.CharField(max_length=200, default='하나아트갤러리', verbose_name='장소')
    venue_address = models.CharField(max_length=500, blank=True, verbose_name='주소')
    
    # 상태
    is_current = models.BooleanField(default=False, verbose_name='현재 전시')
    is_featured = models.BooleanField(default=False, verbose_name='대표 전시')
    is_published = models.BooleanField(default=True, verbose_name='게시 여부')
    
    # SEO
    slug = models.SlugField(unique=True, verbose_name='슬러그')
    meta_description = models.TextField(blank=True, verbose_name='메타 설명')
    
    class Meta:
        verbose_name = '전시'
        verbose_name_plural = '전시 목록'
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title
    
    def is_ongoing(self):
        """현재 진행중인지 확인"""
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date
    
    def is_upcoming(self):
        """예정된 전시인지 확인"""
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date > today
    
    def get_related_exhibitions(self):
        """관련 전시 가져오기"""
        return Exhibition.objects.exclude(id=self.id).filter(is_published=True)[:3]

class Artwork(TimeStampedModel):
    """작품 모델"""
    ARTWORK_TYPES = [
        ('painting', '회화'),
        ('sculpture', '조각'),
        ('photography', '사진'),
        ('installation', '설치'),
        ('media', '미디어'),
        ('craft', '공예'),
        ('other', '기타'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='작품명')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='영문 작품명')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artworks', verbose_name='작가')
    
    artwork_type = models.CharField(max_length=20, choices=ARTWORK_TYPES, default='painting', verbose_name='작품 유형')
    
    # 작품 정보
    year = models.IntegerField(null=True, blank=True, verbose_name='제작년도')
    medium = models.CharField(max_length=200, blank=True, verbose_name='재료/기법')
    size = models.CharField(max_length=100, blank=True, verbose_name='크기')
    edition = models.CharField(max_length=50, blank=True, verbose_name='에디션')
    
    description = models.TextField(blank=True, verbose_name='작품 설명')
    
    # 이미지
    main_image = models.ImageField(upload_to='artworks/', verbose_name='메인 이미지')
    thumbnail = models.ImageField(upload_to='artworks/thumbs/', blank=True, null=True, verbose_name='썸네일')
    
    # 가격 정보
    price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='가격')
    is_sold = models.BooleanField(default=False, verbose_name='판매 완료')
    is_for_sale = models.BooleanField(default=True, verbose_name='판매 가능')
    
    # 전시 연결
    exhibitions = models.ManyToManyField(Exhibition, blank=True, related_name='artworks', verbose_name='전시')
    
    # 상태
    is_featured = models.BooleanField(default=False, verbose_name='대표작품')
    is_published = models.BooleanField(default=True, verbose_name='게시 여부')
    display_order = models.IntegerField(default=0, verbose_name='표시 순서')
    
    class Meta:
        verbose_name = '작품'
        verbose_name_plural = '작품 목록'
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return f'{self.artist.name} - {self.title}'

class ArtworkImage(TimeStampedModel):
    """작품 추가 이미지"""
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='additional_images', verbose_name='작품')
    image = models.ImageField(upload_to='artworks/additional/', verbose_name='이미지')
    caption = models.CharField(max_length=200, blank=True, verbose_name='캡션')
    order = models.IntegerField(default=0, verbose_name='순서')
    
    class Meta:
        verbose_name = '작품 이미지'
        verbose_name_plural = '작품 이미지 목록'
        ordering = ['artwork', 'order']
    
    def __str__(self):
        return f'{self.artwork.title} - Image {self.order}'