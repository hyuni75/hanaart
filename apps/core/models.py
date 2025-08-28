from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class TimeStampedModel(models.Model):
    """기본 타임스탬프 모델"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        abstract = True

class UUIDModel(TimeStampedModel):
    """UUID 기반 모델"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        abstract = True
