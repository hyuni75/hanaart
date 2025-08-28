from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.core.models import TimeStampedModel

class Comment(TimeStampedModel):
    """댓글 모델"""
    # Generic relation으로 어떤 모델에도 댓글 달 수 있게
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # 댓글 내용
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    author_name = models.CharField(max_length=50, blank=True, verbose_name='작성자명(비회원)')
    author_email = models.EmailField(blank=True, verbose_name='이메일(비회원)')
    content = models.TextField(verbose_name='내용')
    
    # 대댓글
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    # 상태
    is_approved = models.BooleanField(default=True, verbose_name='승인 여부')
    is_deleted = models.BooleanField(default=False, verbose_name='삭제 여부')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP 주소')
    
    # 필터링
    is_filtered = models.BooleanField(default=False, verbose_name='필터링됨')
    filtered_reason = models.CharField(max_length=200, blank=True, verbose_name='필터링 사유')
    
    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return f'{self.author.username}: {self.content[:50]}'

class Like(TimeStampedModel):
    """좋아요 모델"""
    # Generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP 주소')
    
    class Meta:
        verbose_name = '좋아요'
        verbose_name_plural = '좋아요 목록'
        # 같은 사용자가 같은 대상에 중복 좋아요 방지
        unique_together = ('content_type', 'object_id', 'user')
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return f'{self.user.username} likes {self.content_object}'

class View(TimeStampedModel):
    """조회수 모델"""
    # Generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='사용자')
    ip_address = models.GenericIPAddressField(verbose_name='IP 주소')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    
    class Meta:
        verbose_name = '조회'
        verbose_name_plural = '조회 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        return f'View on {self.content_object}'

class InteractionSetting(TimeStampedModel):
    """상호작용 설정"""
    SCOPE_CHOICES = [
        ('global', '전체 시스템'),
        ('menu', '메뉴 단위'),
        ('page', '페이지 단위'),
    ]
    
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, default='global', verbose_name='적용 범위')
    
    # 관련 대상 (scope에 따라)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # 설정
    enable_comments = models.BooleanField(default=True, verbose_name='댓글 허용')
    enable_likes = models.BooleanField(default=True, verbose_name='좋아요 허용')
    enable_views = models.BooleanField(default=True, verbose_name='조회수 표시')
    
    # 댓글 설정
    require_login_for_comment = models.BooleanField(default=False, verbose_name='댓글 로그인 필수')
    auto_approve_comments = models.BooleanField(default=True, verbose_name='댓글 자동 승인')
    enable_nested_comments = models.BooleanField(default=True, verbose_name='대댓글 허용')
    max_comment_depth = models.IntegerField(default=2, verbose_name='대댓글 최대 깊이')
    
    class Meta:
        verbose_name = '상호작용 설정'
        verbose_name_plural = '상호작용 설정 목록'
        unique_together = ('scope', 'content_type', 'object_id')
    
    def __str__(self):
        if self.scope == 'global':
            return '전체 시스템 설정'
        return f'{self.get_scope_display()} - {self.content_object}'