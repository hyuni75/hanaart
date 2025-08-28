from django.contrib import admin
from .models import Artist, Exhibition, Artwork, ArtworkImage

class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 1
    fields = ['image', 'caption', 'order']

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'is_exclusive', 'is_active', 'display_order']
    list_filter = ['is_exclusive', 'is_active']
    search_fields = ['name', 'name_en', 'bio']
    list_editable = ['is_exclusive', 'is_active', 'display_order']
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'name_en', 'birth_year', 'profile_image')
        }),
        ('약력', {
            'fields': ('bio', 'education', 'awards')
        }),
        ('연락처', {
            'fields': ('email', 'phone', 'website', 'instagram')
        }),
        ('상태', {
            'fields': ('is_exclusive', 'is_active', 'display_order')
        }),
    )

@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'exhibition_type', 'start_date', 'end_date', 'is_current', 'is_featured', 'is_published']
    list_filter = ['exhibition_type', 'is_current', 'is_featured', 'is_published']
    search_fields = ['title', 'title_en', 'description']
    list_editable = ['is_current', 'is_featured', 'is_published']
    date_hierarchy = 'start_date'
    filter_horizontal = ['artists']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'title_en', 'slug', 'exhibition_type', 'artists')
        }),
        ('전시 정보', {
            'fields': ('description', 'poster_image')
        }),
        ('일정', {
            'fields': ('start_date', 'end_date', 'opening_date')
        }),
        ('장소', {
            'fields': ('venue', 'venue_address')
        }),
        ('상태', {
            'fields': ('is_current', 'is_featured', 'is_published')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'artwork_type', 'year', 'price', 'is_sold', 'is_featured', 'is_published']
    list_filter = ['artwork_type', 'artist', 'is_sold', 'is_for_sale', 'is_featured', 'is_published']
    search_fields = ['title', 'title_en', 'description', 'artist__name']
    list_editable = ['is_sold', 'is_featured', 'is_published']
    filter_horizontal = ['exhibitions']
    inlines = [ArtworkImageInline]
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'title_en', 'artist', 'artwork_type')
        }),
        ('작품 정보', {
            'fields': ('year', 'medium', 'size', 'edition', 'description')
        }),
        ('이미지', {
            'fields': ('main_image', 'thumbnail')
        }),
        ('가격 정보', {
            'fields': ('price', 'is_sold', 'is_for_sale')
        }),
        ('전시', {
            'fields': ('exhibitions',)
        }),
        ('상태', {
            'fields': ('is_featured', 'is_published', 'display_order')
        }),
    )