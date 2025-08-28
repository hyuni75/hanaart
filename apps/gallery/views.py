from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Artist, Exhibition, Artwork

def artist_list(request):
    """작가 목록"""
    artists = Artist.objects.filter(is_active=True).order_by('display_order', 'name')
    
    # 전속작가와 일반작가 분리
    exclusive_artists = artists.filter(is_exclusive=True)
    regular_artists = artists.filter(is_exclusive=False)
    
    context = {
        'exclusive_artists': exclusive_artists,
        'regular_artists': regular_artists,
    }
    return render(request, 'gallery/artist_list.html', context)

def artist_detail(request, pk):
    """작가 상세"""
    artist = get_object_or_404(Artist, pk=pk, is_active=True)
    artworks = artist.artworks.filter(is_published=True).order_by('display_order', '-created_at')
    exhibitions = artist.exhibitions.filter(is_published=True).order_by('-start_date')
    
    context = {
        'artist': artist,
        'artworks': artworks,
        'exhibitions': exhibitions,
    }
    return render(request, 'gallery/artist_detail.html', context)

def exhibition_list(request):
    """전시 목록"""
    exhibitions = Exhibition.objects.filter(is_published=True).order_by('-start_date')
    
    # 현재 전시와 지난 전시 분리
    current_exhibitions = exhibitions.filter(is_current=True)
    past_exhibitions = exhibitions.filter(is_current=False)
    
    # 페이지네이션
    paginator = Paginator(past_exhibitions, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'current_exhibitions': current_exhibitions,
        'page_obj': page_obj,
    }
    return render(request, 'gallery/exhibition_list.html', context)

def exhibition_detail(request, slug):
    """전시 상세"""
    exhibition = get_object_or_404(Exhibition, slug=slug, is_published=True)
    artworks = exhibition.artworks.filter(is_published=True).order_by('display_order')
    
    context = {
        'exhibition': exhibition,
        'artworks': artworks,
    }
    return render(request, 'gallery/exhibition_detail.html', context)

def artwork_detail(request, pk):
    """작품 상세"""
    artwork = get_object_or_404(Artwork, pk=pk, is_published=True)
    related_artworks = Artwork.objects.filter(
        artist=artwork.artist,
        is_published=True
    ).exclude(pk=pk)[:4]
    
    context = {
        'artwork': artwork,
        'related_artworks': related_artworks,
    }
    return render(request, 'gallery/artwork_detail.html', context)

def location(request):
    """오시는길"""
    return render(request, 'gallery/location.html')

def frame(request):
    """맞춤 액자제작"""
    return render(request, 'gallery/frame.html')
