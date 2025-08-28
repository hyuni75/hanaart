from django.contrib import admin
from .models import Template, Page, Block, Media

class BlockInline(admin.StackedInline):
    model = Block
    extra = 1
    fields = ['block_type', 'title', 'content', 'order', 'css_class', 'is_visible']
    ordering = ['order']

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'template_type', 'is_active', 'created_at']
    list_filter = ['template_type', 'is_active']
    search_fields = ['name', 'slug', 'description']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'slug', 'template_type', 'description')
        }),
        ('템플릿 코드', {
            'fields': ('html_template', 'css_styles'),
            'classes': ('collapse',)
        }),
        ('상태', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'template', 'is_published', 'enable_comments', 'enable_likes', 'created_at']
    list_filter = ['is_published', 'template', 'enable_comments', 'enable_likes']
    search_fields = ['title', 'slug', 'meta_description']
    list_editable = ['is_published', 'enable_comments', 'enable_likes']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlockInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'slug', 'template')
        }),
        ('게시 설정', {
            'fields': ('is_published', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('상호작용 설정', {
            'fields': ('enable_comments', 'enable_likes')
        }),
    )

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['page', 'block_type', 'title', 'order', 'is_visible']
    list_filter = ['block_type', 'is_visible', 'page']
    search_fields = ['title', 'content', 'page__title']
    list_editable = ['order', 'is_visible']
    ordering = ['page', 'order']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('page', 'block_type', 'title')
        }),
        ('콘텐츠', {
            'fields': ('content', 'settings_json')
        }),
        ('레이아웃', {
            'fields': ('order', 'css_class', 'is_visible')
        }),
    )

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['name', 'media_type', 'file', 'uploaded_by', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['name', 'alt_text', 'caption']
    date_hierarchy = 'created_at'
    readonly_fields = ['file_size', 'width', 'height', 'created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'file', 'media_type')
        }),
        ('설명', {
            'fields': ('alt_text', 'caption')
        }),
        ('메타데이터', {
            'fields': ('file_size', 'width', 'height', 'uploaded_by'),
            'classes': ('collapse',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)