from django.contrib import admin
from .models import Comment, Like, View, InteractionSetting

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_content_preview', 'author', 'is_approved', 'is_filtered', 'created_at']
    list_filter = ['is_approved', 'is_deleted', 'is_filtered', 'created_at']
    search_fields = ['content', 'author__username', 'author_name']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'ip_address']
    
    fieldsets = (
        ('콘텐츠', {
            'fields': ('content_type', 'object_id', 'content')
        }),
        ('작성자', {
            'fields': ('author', 'author_name', 'author_email')
        }),
        ('관계', {
            'fields': ('parent',)
        }),
        ('상태', {
            'fields': ('is_approved', 'is_deleted')
        }),
        ('필터링', {
            'fields': ('is_filtered', 'filtered_reason'),
            'classes': ('collapse',)
        }),
        ('메타데이터', {
            'fields': ('ip_address', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    get_content_preview.short_description = '내용'
    
    actions = ['approve_comments', 'delete_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()}개의 댓글이 승인되었습니다.")
    approve_comments.short_description = "선택한 댓글 승인"
    
    def delete_comments(self, request, queryset):
        queryset.update(is_deleted=True)
        self.message_user(request, f"{queryset.count()}개의 댓글이 삭제되었습니다.")
    delete_comments.short_description = "선택한 댓글 삭제"

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'created_at']
    list_filter = ['content_type', 'created_at']
    search_fields = ['user__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'ip_address']

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', 'user', 'ip_address', 'created_at']
    list_filter = ['content_type', 'created_at']
    search_fields = ['user__username', 'ip_address']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(InteractionSetting)
class InteractionSettingAdmin(admin.ModelAdmin):
    list_display = ['scope', 'enable_comments', 'enable_likes', 'enable_views', 'require_login_for_comment']
    list_filter = ['scope', 'enable_comments', 'enable_likes', 'enable_views']
    list_editable = ['enable_comments', 'enable_likes', 'enable_views', 'require_login_for_comment']
    
    fieldsets = (
        ('범위', {
            'fields': ('scope', 'content_type', 'object_id')
        }),
        ('기본 설정', {
            'fields': ('enable_comments', 'enable_likes', 'enable_views')
        }),
        ('댓글 설정', {
            'fields': ('require_login_for_comment', 'auto_approve_comments', 
                      'enable_nested_comments', 'max_comment_depth')
        }),
    )