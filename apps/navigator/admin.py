from django.contrib import admin
from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'menu_type', 'order', 'is_active', 'is_visible', 'created_at']
    list_filter = ['menu_type', 'is_active', 'is_visible']
    search_fields = ['title', 'slug', 'url']
    list_editable = ['order', 'is_active', 'is_visible']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'title']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'slug', 'parent', 'menu_type', 'url')
        }),
        ('표시 설정', {
            'fields': ('icon', 'order', 'is_active', 'is_visible', 'target_blank')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
