# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Template, TemplateSection, Artist, Artwork, Exhibition, ExhibitionArtwork, ArtFair, History


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['template_name', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'template_name']
    search_fields = ['template_name']


@admin.register(TemplateSection)
class TemplateSectionAdmin(admin.ModelAdmin):
    list_display = ['template', 'section_name', 'section_type', 'order', 'is_active']
    list_filter = ['template', 'section_type', 'is_active']
    search_fields = ['section_name', 'title', 'content']
    list_editable = ['order', 'is_active']


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_en', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'name_en', 'description']
    list_editable = ['order', 'is_active']


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'year', 'is_featured', 'order', 'is_active', 'created_at']
    list_filter = ['artist', 'is_featured', 'is_active', 'year']
    search_fields = ['title', 'title_en', 'description']
    list_editable = ['order', 'is_featured', 'is_active']
    raw_id_fields = ['artist']


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'start_date', 'end_date', 'is_active', 'created_at']
    list_filter = ['artist', 'is_active', 'start_date']
    search_fields = ['title', 'description']
    raw_id_fields = ['artist']
    date_hierarchy = 'start_date'


@admin.register(ExhibitionArtwork)
class ExhibitionArtworkAdmin(admin.ModelAdmin):
    list_display = ['exhibition', 'artwork', 'order', 'created_at']
    list_filter = ['exhibition']
    search_fields = ['exhibition__title', 'artwork__title']
    list_editable = ['order']
    raw_id_fields = ['exhibition', 'artwork']


@admin.register(ArtFair)
class ArtFairAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'order', 'is_active', 'created_at']
    list_filter = ['year', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['year', 'content', 'order', 'is_active']
    list_filter = ['year', 'is_active']
    search_fields = ['content']
    list_editable = ['order', 'is_active']
