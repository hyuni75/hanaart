# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def resize_image(image_field, max_width=1920, max_height=1080, quality=85):
    """이미지 리사이징 헬퍼 함수 - 용량 최적화"""
    if not image_field:
        return None

    img = Image.open(image_field)

    # EXIF 방향 정보 처리
    try:
        from PIL import ImageOps
        img = ImageOps.exif_transpose(img)
    except:
        pass

    # 원본 크기 확인
    width, height = img.size

    # 최대 크기를 초과하는 경우에만 리사이징
    if width > max_width or height > max_height:
        # 비율 유지하면서 리사이징
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

    # RGB 모드로 변환 (RGBA 이미지 처리)
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background

    # BytesIO로 저장
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)

    # 새 파일명 생성
    file_name = image_field.name.split('/')[-1]
    file_name = file_name.rsplit('.', 1)[0] + '.jpg'

    return InMemoryUploadedFile(
        output, 'ImageField', file_name, 'image/jpeg',
        sys.getsizeof(output), None
    )


class Template(models.Model):
    """템플릿 관리 모델"""
    TEMPLATE_CHOICES = [
        ('home', '홈'),
        ('about', '인사말'),
        ('history', '연혁'),
        ('exhibition', '전시'),
        ('artfair', '아트페어'),
        ('artist', '작가'),
        ('frame', '액자제작'),
        ('contact', '연락처'),
    ]

    template_name = models.CharField('템플릿명', max_length=50, choices=TEMPLATE_CHOICES, unique=True)
    is_active = models.BooleanField('활성화', default=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '템플릿'
        verbose_name_plural = '템플릿 목록'
        ordering = ['template_name']

    def __str__(self):
        return self.get_template_name_display()


class TemplateSection(models.Model):
    """템플릿 섹션 관리 모델"""
    SECTION_TYPE_CHOICES = [
        ('text', '텍스트'),
        ('image', '이미지'),
        ('gallery', '갤러리'),
        ('list', '리스트'),
    ]

    template = models.ForeignKey(Template, on_delete=models.CASCADE, verbose_name='템플릿', related_name='sections')
    section_name = models.CharField('섹션명', max_length=100)
    section_type = models.CharField('섹션 타입', max_length=20, choices=SECTION_TYPE_CHOICES)
    title = models.CharField('제목', max_length=200, blank=True)
    content = models.TextField('내용', blank=True)
    order = models.IntegerField('정렬순서', default=0)
    is_active = models.BooleanField('활성화', default=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '템플릿 섹션'
        verbose_name_plural = '템플릿 섹션 목록'
        ordering = ['template', 'order']

    def __str__(self):
        return f'{self.template} - {self.section_name}'


class Artist(models.Model):
    """작가 관리 모델"""
    name = models.CharField('작가명', max_length=100)
    name_en = models.CharField('영문명', max_length=100, blank=True)
    description = models.TextField('작가 설명')
    profile_image = models.ImageField('프로필 이미지', upload_to='artists/', blank=True, null=True)
    order = models.IntegerField('정렬순서', default=0)
    is_active = models.BooleanField('활성화', default=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '작가'
        verbose_name_plural = '작가 목록'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """저장 시 이미지 리사이징"""
        if self.profile_image:
            resized = resize_image(self.profile_image, max_width=800, max_height=800, quality=90)
            if resized:
                self.profile_image = resized
        super().save(*args, **kwargs)


class Artwork(models.Model):
    """작품 관리 모델"""
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='작가', related_name='artworks')
    title = models.CharField('작품명', max_length=200)
    title_en = models.CharField('영문 작품명', max_length=200, blank=True)
    description = models.TextField('작품 설명', blank=True)
    image = models.ImageField('작품 이미지', upload_to='artworks/')
    year = models.IntegerField('제작년도', blank=True, null=True)
    size = models.CharField('크기', max_length=100, blank=True)
    material = models.CharField('재료', max_length=200, blank=True)
    order = models.IntegerField('정렬순서', default=0)
    is_featured = models.BooleanField('메인 히어로 노출', default=False, help_text='홈 페이지 히어로 섹션에 노출됩니다')
    is_active = models.BooleanField('활성화', default=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '작품'
        verbose_name_plural = '작품 목록'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f'{self.artist.name} - {self.title}'

    def save(self, *args, **kwargs):
        """저장 시 이미지 리사이징"""
        if self.image:
            resized = resize_image(self.image, max_width=1920, max_height=1080, quality=85)
            if resized:
                self.image = resized
        super().save(*args, **kwargs)


class Exhibition(models.Model):
    """전시 관리 모델"""
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='작가', related_name='exhibitions')
    title = models.CharField('전시명', max_length=200)
    title_en = models.CharField('영문 전시명', max_length=200, blank=True)
    description = models.TextField('전시 설명')
    location = models.CharField('전시 장소', max_length=200, blank=True)
    start_date = models.DateField('전시 시작일')
    end_date = models.DateField('전시 종료일')
    poster_image = models.ImageField('포스터 이미지', upload_to='exhibitions/', blank=True, null=True)
    order = models.IntegerField('정렬순서', default=0)
    is_active = models.BooleanField('활성화', default=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '전시'
        verbose_name_plural = '전시 목록'
        ordering = ['order', '-start_date']

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        """진행 중인 전시 여부"""
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def save(self, *args, **kwargs):
        """저장 시 포스터 이미지 리사이징 - 썸네일 최적화"""
        if self.poster_image:
            # 카드 썸네일용으로 작게 리사이징 (800x600, 품질 80)
            resized = resize_image(self.poster_image, max_width=800, max_height=600, quality=80)
            if resized:
                self.poster_image = resized
        super().save(*args, **kwargs)


class ExhibitionArtwork(models.Model):
    """전시-작품 연결 모델"""
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, verbose_name='전시', related_name='exhibition_artworks')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, verbose_name='작품', related_name='exhibition_artworks')
    order = models.IntegerField('정렬순서', default=0)
    created_at = models.DateTimeField('생성일', auto_now_add=True)

    class Meta:
        verbose_name = '전시 작품'
        verbose_name_plural = '전시 작품 목록'
        ordering = ['exhibition', 'order']
        unique_together = ['exhibition', 'artwork']

    def __str__(self):
        return f'{self.exhibition.title} - {self.artwork.title}'


class ArtFair(models.Model):
    """아트페어 관리 모델"""
    title = models.CharField('아트페어명', max_length=200)
    description = models.TextField('설명')
    year = models.IntegerField('연도')
    image = models.ImageField('이미지', upload_to='artfairs/')
    order = models.IntegerField('정렬순서', default=0)
    is_active = models.BooleanField('활성화', default=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '아트페어'
        verbose_name_plural = '아트페어 목록'
        ordering = ['-year', 'order']

    def __str__(self):
        return f'{self.year} - {self.title}'


class History(models.Model):
    """연혁 관리 모델"""
    year = models.IntegerField('연도')
    content = models.TextField('내용')
    order = models.IntegerField('정렬순서', default=0)
    is_active = models.BooleanField('활성화', default=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '연혁'
        verbose_name_plural = '연혁 목록'
        ordering = ['year', 'order']

    def __str__(self):
        return f'{self.year}'


class About(models.Model):
    """인사말 관리 모델"""
    title = models.CharField('제목', max_length=200, default='인사말')
    content_1 = models.TextField('첫 번째 문단')
    content_2 = models.TextField('두 번째 문단')
    content_3 = models.TextField('세 번째 문단')
    image_1 = models.ImageField('전시장 내부 이미지', upload_to='about/', blank=True, null=True)
    image_1_title = models.CharField('이미지1 제목', max_length=100, default='전시장 내부')
    image_1_desc = models.CharField('이미지1 설명', max_length=200, default='하나아트갤러리 전시 공간')
    image_2 = models.ImageField('전시장 도면 이미지', upload_to='about/', blank=True, null=True)
    image_2_title = models.CharField('이미지2 제목', max_length=100, default='전시장 도면')
    image_2_desc = models.CharField('이미지2 설명', max_length=200, default='갤러리 평면도')
    is_active = models.BooleanField('활성화', default=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '인사말'
        verbose_name_plural = '인사말 목록'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """저장 시 이미지 리사이징"""
        if self.image_1:
            resized = resize_image(self.image_1, max_width=1200, max_height=800)
            if resized:
                self.image_1 = resized

        if self.image_2:
            resized = resize_image(self.image_2, max_width=1200, max_height=800)
            if resized:
                self.image_2 = resized

        super().save(*args, **kwargs)


class Frame(models.Model):
    """액자제작 관리 모델 - 1개 항목에 3개 이미지"""
    title = models.CharField('제목', max_length=200, default='액자 제작')
    description = models.TextField('설명')
    image_1 = models.ImageField('액자 이미지 1', upload_to='frames/')
    image_2 = models.ImageField('액자 이미지 2', upload_to='frames/', blank=True, null=True)
    image_3 = models.ImageField('액자 이미지 3', upload_to='frames/', blank=True, null=True)
    order = models.IntegerField('정렬순서', default=0)
    is_active = models.BooleanField('활성화', default=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '액자'
        verbose_name_plural = '액자 목록'
        ordering = ['order']

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        """저장 시 이미지 리사이징"""
        if self.image_1:
            resized = resize_image(self.image_1, max_width=1200, max_height=900, quality=85)
            if resized:
                self.image_1 = resized

        if self.image_2:
            resized = resize_image(self.image_2, max_width=1200, max_height=900, quality=85)
            if resized:
                self.image_2 = resized

        if self.image_3:
            resized = resize_image(self.image_3, max_width=1200, max_height=900, quality=85)
            if resized:
                self.image_3 = resized

        super().save(*args, **kwargs)


class Contact(models.Model):
    """연락처 관리 모델"""
    title = models.CharField('제목', max_length=200, default='하나아트갤러리 본점(인사동)')
    ceo_name = models.CharField('대표자명', max_length=100)
    ceo_name_en = models.CharField('대표자 영문명', max_length=100, blank=True)
    phone = models.CharField('전화번호', max_length=50)
    fax = models.CharField('팩스번호', max_length=50, blank=True)
    mobile = models.CharField('휴대전화', max_length=50, blank=True)
    email = models.EmailField('이메일')
    address = models.TextField('주소')
    address_en = models.TextField('영문 주소', blank=True)
    is_active = models.BooleanField('활성화', default=True)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '연락처'
        verbose_name_plural = '연락처 목록'

    def __str__(self):
        return self.title


class HomeDesignType(models.Model):
    """홈 디자인 타입 설정 모델 - 수억원급 프리미엄 디자인 3종"""
    DESIGN_CHOICES = [
        ('premium_grid', '프리미엄 그리드 모자이크 (GSAP + Lenis + GLSL Shaders)'),
        ('cube_3d', '3D 큐브 갤러리 (Three.js + WebGL)'),
        ('cinematic', '시네마틱 풀스크린 슬라이더 (영화급 트랜지션)'),
    ]

    design_type = models.CharField(
        '디자인 타입',
        max_length=20,
        choices=DESIGN_CHOICES,
        default='premium_grid',
        help_text='수억원급 프리미엄 홈 디자인 선택'
    )
    is_active = models.BooleanField('현재 활성화', default=True)
    updated_at = models.DateTimeField('마지막 변경', auto_now=True)
    updated_by = models.CharField('변경자', max_length=100, blank=True)

    class Meta:
        verbose_name = '홈 디자인 설정'
        verbose_name_plural = '홈 디자인 설정'

    def __str__(self):
        return f'{self.get_design_type_display()}'

    def save(self, *args, **kwargs):
        """저장 시 다른 모든 설정을 비활성화"""
        if self.is_active:
            HomeDesignType.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_active_design(cls):
        """현재 활성화된 디자인 타입 반환"""
        design = cls.objects.filter(is_active=True).first()
        return design.design_type if design else 'premium_grid'
