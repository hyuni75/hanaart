from django.contrib import admin
from .models import FilterRule, BlockedWord, SpamPattern, ModerationLog

@admin.register(FilterRule)
class FilterRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'rule_type', 'pattern', 'action', 'severity', 'is_active', 'match_count']
    list_filter = ['rule_type', 'action', 'severity', 'is_active']
    search_fields = ['name', 'pattern', 'description']
    list_editable = ['action', 'severity', 'is_active']
    ordering = ['-severity', 'name']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'rule_type', 'pattern', 'replacement')
        }),
        ('액션 설정', {
            'fields': ('action', 'severity', 'description')
        }),
        ('옵션', {
            'fields': ('is_active', 'is_case_sensitive')
        }),
        ('통계', {
            'fields': ('match_count',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['match_count']

@admin.register(BlockedWord)
class BlockedWordAdmin(admin.ModelAdmin):
    list_display = ['word', 'category', 'severity', 'is_active']
    list_filter = ['category', 'severity', 'is_active']
    search_fields = ['word']
    list_editable = ['category', 'severity', 'is_active']
    ordering = ['category', 'word']

@admin.register(SpamPattern)
class SpamPatternAdmin(admin.ModelAdmin):
    list_display = ['name', 'pattern', 'is_regex', 'is_active', 'detection_count']
    list_filter = ['is_regex', 'is_active']
    search_fields = ['name', 'pattern', 'description']
    list_editable = ['is_active']
    readonly_fields = ['detection_count']

@admin.register(ModerationLog)
class ModerationLogAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'result', 'user', 'is_reviewed', 'created_at']
    list_filter = ['content_type', 'result', 'is_reviewed', 'created_at']
    search_fields = ['original_content', 'filtered_content', 'user__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('콘텐츠', {
            'fields': ('content_type', 'original_content', 'filtered_content')
        }),
        ('매칭 정보', {
            'fields': ('matched_rules', 'matched_words', 'result')
        }),
        ('사용자 정보', {
            'fields': ('user', 'ip_address', 'user_agent')
        }),
        ('검토', {
            'fields': ('is_reviewed', 'reviewed_by', 'reviewed_at', 'review_notes')
        }),
        ('시간', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if obj.is_reviewed and not obj.reviewed_by:
            obj.reviewed_by = request.user
        super().save_model(request, obj, form, change)