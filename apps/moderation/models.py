from django.db import models
from apps.core.models import TimeStampedModel
import re

class FilterRule(TimeStampedModel):
    """필터링 규칙"""
    RULE_TYPES = [
        ('word', '단어'),
        ('pattern', '패턴'),
        ('regex', '정규식'),
        ('url', 'URL'),
    ]
    
    ACTIONS = [
        ('block', '차단'),
        ('replace', '대체'),
        ('review', '검토'),
        ('warning', '경고'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='규칙 이름')
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES, default='word', verbose_name='규칙 타입')
    pattern = models.CharField(max_length=500, verbose_name='패턴')
    replacement = models.CharField(max_length=100, default='***', blank=True, verbose_name='대체 텍스트')
    action = models.CharField(max_length=20, choices=ACTIONS, default='replace', verbose_name='액션')
    
    description = models.TextField(blank=True, verbose_name='설명')
    severity = models.IntegerField(default=1, verbose_name='심각도 (1-10)')
    
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    is_case_sensitive = models.BooleanField(default=False, verbose_name='대소문자 구분')
    
    # 통계
    match_count = models.IntegerField(default=0, verbose_name='매칭 횟수')
    
    class Meta:
        verbose_name = '필터 규칙'
        verbose_name_plural = '필터 규칙 목록'
        ordering = ['-severity', 'name']
    
    def __str__(self):
        return f'{self.name} ({self.get_rule_type_display()})'
    
    def check_content(self, text):
        """텍스트 검사"""
        if not self.is_active:
            return False, text
        
        flags = 0 if self.is_case_sensitive else re.IGNORECASE
        
        if self.rule_type == 'word':
            # 단어 경계를 포함한 패턴
            pattern = r'\b' + re.escape(self.pattern) + r'\b'
        elif self.rule_type == 'pattern':
            pattern = re.escape(self.pattern)
        elif self.rule_type == 'regex':
            pattern = self.pattern
        elif self.rule_type == 'url':
            # URL 패턴 감지
            pattern = r'https?://[^\s]+'
        else:
            return False, text
        
        try:
            if re.search(pattern, text, flags):
                self.match_count += 1
                self.save()
                
                if self.action == 'block':
                    return True, None
                elif self.action == 'replace':
                    new_text = re.sub(pattern, self.replacement, text, flags=flags)
                    return True, new_text
                elif self.action in ['review', 'warning']:
                    return True, text
        except:
            pass
        
        return False, text

class BlockedWord(TimeStampedModel):
    """금지어"""
    word = models.CharField(max_length=100, unique=True, verbose_name='금지어')
    category = models.CharField(max_length=50, default='general', verbose_name='카테고리')
    severity = models.IntegerField(default=5, verbose_name='심각도 (1-10)')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    
    class Meta:
        verbose_name = '금지어'
        verbose_name_plural = '금지어 목록'
        ordering = ['category', 'word']
    
    def __str__(self):
        return self.word

class SpamPattern(TimeStampedModel):
    """스팸 패턴"""
    name = models.CharField(max_length=100, verbose_name='패턴 이름')
    pattern = models.TextField(verbose_name='패턴')
    description = models.TextField(blank=True, verbose_name='설명')
    is_regex = models.BooleanField(default=False, verbose_name='정규식 여부')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    
    # 통계
    detection_count = models.IntegerField(default=0, verbose_name='감지 횟수')
    
    class Meta:
        verbose_name = '스팸 패턴'
        verbose_name_plural = '스팸 패턴 목록'
    
    def __str__(self):
        return self.name

class ModerationLog(TimeStampedModel):
    """검열 로그"""
    CONTENT_TYPES = [
        ('comment', '댓글'),
        ('post', '게시물'),
        ('message', '메시지'),
        ('other', '기타'),
    ]
    
    RESULTS = [
        ('passed', '통과'),
        ('blocked', '차단'),
        ('replaced', '대체'),
        ('review', '검토 대기'),
        ('warning', '경고'),
    ]
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, verbose_name='콘텐츠 타입')
    original_content = models.TextField(verbose_name='원본 내용')
    filtered_content = models.TextField(blank=True, verbose_name='필터링된 내용')
    
    matched_rules = models.ManyToManyField(FilterRule, blank=True, verbose_name='매칭된 규칙')
    matched_words = models.ManyToManyField(BlockedWord, blank=True, verbose_name='매칭된 금지어')
    
    result = models.CharField(max_length=20, choices=RESULTS, verbose_name='결과')
    
    # 사용자 정보
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='사용자')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP 주소')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    
    # 처리 정보
    is_reviewed = models.BooleanField(default=False, verbose_name='검토 완료')
    reviewed_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_logs', verbose_name='검토자')
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='검토일')
    review_notes = models.TextField(blank=True, verbose_name='검토 노트')
    
    class Meta:
        verbose_name = '검열 로그'
        verbose_name_plural = '검열 로그 목록'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.get_content_type_display()} - {self.get_result_display()}'

class ContentFilter:
    """콘텐츠 필터링 헬퍼 클래스"""
    
    @staticmethod
    def check(text, content_type='comment'):
        """
        텍스트 검사
        Returns: (is_clean, filtered_text, matched_rules, action)
        """
        if not text:
            return True, text, [], 'passed'
        
        matched_rules = []
        filtered_text = text
        action = 'passed'
        
        # 필터 규칙 체크
        for rule in FilterRule.objects.filter(is_active=True).order_by('-severity'):
            matched, new_text = rule.check_content(filtered_text)
            if matched:
                matched_rules.append(rule)
                if rule.action == 'block':
                    action = 'blocked'
                    break
                elif rule.action == 'replace':
                    filtered_text = new_text
                    action = 'replaced'
                elif rule.action == 'review' and action not in ['blocked', 'replaced']:
                    action = 'review'
                elif rule.action == 'warning' and action == 'passed':
                    action = 'warning'
        
        # 금지어 체크
        for word in BlockedWord.objects.filter(is_active=True):
            if word.word.lower() in filtered_text.lower():
                matched_rules.append(word)
                filtered_text = filtered_text.replace(word.word, '***')
                if action == 'passed':
                    action = 'replaced'
        
        # 스팸 패턴 체크
        for pattern in SpamPattern.objects.filter(is_active=True):
            try:
                if pattern.is_regex:
                    if re.search(pattern.pattern, filtered_text):
                        pattern.detection_count += 1
                        pattern.save()
                        action = 'blocked'
                        break
                else:
                    if pattern.pattern in filtered_text:
                        pattern.detection_count += 1
                        pattern.save()
                        action = 'blocked'
                        break
            except:
                pass
        
        is_clean = action == 'passed'
        
        return is_clean, filtered_text, matched_rules, action