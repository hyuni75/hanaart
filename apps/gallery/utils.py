from PIL import Image
import os
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO

class ImageOptimizer:
    """이미지 최적화 유틸리티"""
    
    THUMBNAIL_SIZE = (300, 300)
    MEDIUM_SIZE = (800, 800)
    LARGE_SIZE = (1920, 1920)
    
    @classmethod
    def create_thumbnail(cls, image_file, quality=85):
        """썸네일 생성"""
        img = Image.open(image_file)
        
        # RGBA를 RGB로 변환
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # 썸네일 생성
        img.thumbnail(cls.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
        
        # BytesIO에 저장
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return ContentFile(output.read())
    
    @classmethod
    def create_medium(cls, image_file, quality=90):
        """중간 크기 이미지 생성"""
        img = Image.open(image_file)
        
        # RGBA를 RGB로 변환
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # 리사이즈
        img.thumbnail(cls.MEDIUM_SIZE, Image.Resampling.LANCZOS)
        
        # BytesIO에 저장
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return ContentFile(output.read())
    
    @classmethod
    def optimize_large(cls, image_file, quality=95):
        """큰 이미지 최적화"""
        img = Image.open(image_file)
        
        # RGBA를 RGB로 변환
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # 너무 큰 이미지만 리사이즈
        if img.width > cls.LARGE_SIZE[0] or img.height > cls.LARGE_SIZE[1]:
            img.thumbnail(cls.LARGE_SIZE, Image.Resampling.LANCZOS)
        
        # BytesIO에 저장
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True, progressive=True)
        output.seek(0)
        
        return ContentFile(output.read())
    
    @classmethod
    def get_image_dimensions(cls, image_file):
        """이미지 크기 반환"""
        img = Image.open(image_file)
        return img.width, img.height
    
    @classmethod
    def process_artwork_image(cls, artwork_image):
        """작품 이미지 처리 - 3가지 버전 생성"""
        original = artwork_image.image.file
        
        # 파일명 생성
        base_name = os.path.splitext(artwork_image.image.name)[0]
        
        # 썸네일 생성
        thumbnail = cls.create_thumbnail(original)
        thumbnail_name = f"{base_name}_thumb.jpg"
        
        # 중간 크기 생성
        original.seek(0)  # 파일 포인터 리셋
        medium = cls.create_medium(original)
        medium_name = f"{base_name}_medium.jpg"
        
        # 큰 이미지 최적화
        original.seek(0)  # 파일 포인터 리셋
        large = cls.optimize_large(original)
        large_name = f"{base_name}_large.jpg"
        
        return {
            'thumbnail': (thumbnail_name, thumbnail),
            'medium': (medium_name, medium),
            'large': (large_name, large)
        }
    
    @classmethod
    def create_responsive_set(cls, image_file):
        """반응형 이미지 세트 생성"""
        sizes = [
            (320, 'xs'),   # 모바일
            (640, 'sm'),   # 태블릿
            (1024, 'md'),  # 데스크탑
            (1920, 'lg'),  # 큰 화면
        ]
        
        result = {}
        img = Image.open(image_file)
        
        # RGBA를 RGB로 변환
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        for width, suffix in sizes:
            # 원본보다 큰 사이즈는 건너뛰기
            if width > img.width:
                continue
            
            # 비율 유지하며 리사이즈
            ratio = width / img.width
            height = int(img.height * ratio)
            
            resized = img.resize((width, height), Image.Resampling.LANCZOS)
            
            output = BytesIO()
            resized.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            result[suffix] = ContentFile(output.read())
        
        return result