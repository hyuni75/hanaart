from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Artist, Exhibition, Artwork
from .forms import ArtistForm, ExhibitionForm, ArtworkForm

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

# Admin Dashboard
@login_required
def admin_dashboard(request):
    """관리자 대시보드"""
    context = {
        'total_artists': Artist.objects.count(),
        'total_exhibitions': Exhibition.objects.count(),
        'total_artworks': Artwork.objects.count(),
        'recent_artists': Artist.objects.order_by('-created_at')[:6],
        'recent_exhibitions': Exhibition.objects.order_by('-created_at')[:5],
        'current_exhibitions': Exhibition.objects.filter(is_current=True),
    }
    return render(request, 'admin/gallery_dashboard.html', context)

# Artist CRUD Views
@login_required
def artist_manage_list(request):
    """작가 관리 목록"""
    artists = Artist.objects.all().order_by('display_order', 'name')
    paginator = Paginator(artists, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'admin/artist_list.html', context)

@login_required
def artist_create(request):
    """작가 생성"""
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            artist = form.save()
            messages.success(request, f'작가 {artist.name}이(가) 등록되었습니다.')
            return redirect('gallery:artist_manage_list')
    else:
        form = ArtistForm()
    
    context = {
        'form': form,
        'title': '작가 등록',
    }
    return render(request, 'admin/artist_form.html', context)

@login_required
def artist_edit(request, pk):
    """작가 수정"""
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            messages.success(request, f'작가 {artist.name}이(가) 수정되었습니다.')
            return redirect('gallery:artist_manage_list')
    else:
        form = ArtistForm(instance=artist)
    
    context = {
        'form': form,
        'title': f'작가 수정 - {artist.name}',
        'artist': artist,
    }
    return render(request, 'admin/artist_form.html', context)

@login_required
@require_POST
def artist_delete(request, pk):
    """작가 삭제"""
    artist = get_object_or_404(Artist, pk=pk)
    name = artist.name
    
    try:
        # 작가에게 연결된 작품이 있는지 확인
        if artist.artworks.exists():
            error_msg = f'{name} 작가는 {artist.artworks.count()}개의 작품이 등록되어 있어 삭제할 수 없습니다. 먼저 작품을 삭제하거나 다른 작가로 변경해주세요.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': error_msg})
            messages.error(request, error_msg)
            return redirect('gallery:artist_manage_list')
        
        artist.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': f'{name} 작가가 삭제되었습니다.'})
        
        messages.success(request, f'{name} 작가가 삭제되었습니다.')
        return redirect('gallery:artist_manage_list')
        
    except Exception as e:
        error_msg = f'삭제 중 오류가 발생했습니다: {str(e)}'
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': error_msg})
        messages.error(request, error_msg)
        return redirect('gallery:artist_manage_list')

# Exhibition CRUD Views
@login_required
def exhibition_manage_list(request):
    """전시 관리 목록"""
    exhibitions = Exhibition.objects.all().order_by('-start_date')
    paginator = Paginator(exhibitions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'admin/exhibition_list.html', context)

@login_required
def exhibition_create(request):
    """전시 생성"""
    if request.method == 'POST':
        form = ExhibitionForm(request.POST, request.FILES)
        if form.is_valid():
            exhibition = form.save()
            # 선택된 작품들을 전시와 연결
            if form.cleaned_data.get('artworks'):
                artworks = form.cleaned_data['artworks']
                for artwork in artworks:
                    artwork.exhibitions.add(exhibition)
            messages.success(request, f'전시 {exhibition.title}이(가) 등록되었습니다.')
            return redirect('gallery:exhibition_manage_list')
    else:
        form = ExhibitionForm()
    
    context = {
        'form': form,
        'title': '전시 등록',
    }
    return render(request, 'admin/exhibition_form.html', context)

@login_required
def exhibition_edit(request, pk):
    """전시 수정"""
    exhibition = get_object_or_404(Exhibition, pk=pk)
    if request.method == 'POST':
        form = ExhibitionForm(request.POST, request.FILES, instance=exhibition)
        if form.is_valid():
            exhibition = form.save()
            # 기존 작품 연결 해제 후 새로 선택된 작품들 연결
            exhibition.artworks.clear()
            if form.cleaned_data.get('artworks'):
                artworks = form.cleaned_data['artworks']
                for artwork in artworks:
                    artwork.exhibitions.add(exhibition)
            messages.success(request, f'전시 {exhibition.title}이(가) 수정되었습니다.')
            return redirect('gallery:exhibition_manage_list')
    else:
        form = ExhibitionForm(instance=exhibition)
        # 기존 전시에 연결된 작품들을 초기값으로 설정
        form.fields['artworks'].initial = exhibition.artworks.all()
    
    context = {
        'form': form,
        'title': f'전시 수정 - {exhibition.title}',
        'exhibition': exhibition,
    }
    return render(request, 'admin/exhibition_form.html', context)

@login_required
@require_POST
def exhibition_delete(request, pk):
    """전시 삭제"""
    exhibition = get_object_or_404(Exhibition, pk=pk)
    title = exhibition.title
    exhibition.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': f'{title} 전시가 삭제되었습니다.'})
    
    messages.success(request, f'{title} 전시가 삭제되었습니다.')
    return redirect('gallery:exhibition_manage_list')

@login_required
@require_POST
def exhibition_set_current(request, pk):
    """현재 전시 설정"""
    exhibition = get_object_or_404(Exhibition, pk=pk)
    
    # 기존 현재 전시 해제
    Exhibition.objects.filter(is_current=True).update(is_current=False)
    
    # 새로운 현재 전시 설정
    exhibition.is_current = True
    exhibition.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': f'{exhibition.title}이(가) 현재 전시로 설정되었습니다.'})
    
    messages.success(request, f'{exhibition.title}이(가) 현재 전시로 설정되었습니다.')
    return redirect('gallery:exhibition_manage_list')

# Artwork CRUD Views
@login_required
def artwork_manage_list(request):
    """작품 관리 목록"""
    artworks = Artwork.objects.all().select_related('artist').order_by('-created_at')
    paginator = Paginator(artworks, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 필터용 작가 목록
    artists = Artist.objects.filter(is_active=True).order_by('name')
    
    context = {
        'page_obj': page_obj,
        'artists': artists,
    }
    return render(request, 'admin/artwork_list.html', context)

@login_required
def artwork_create(request):
    """작품 생성"""
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save()
            messages.success(request, f'작품 {artwork.title}이(가) 등록되었습니다.')
            return redirect('gallery:artwork_manage_list')
    else:
        form = ArtworkForm()
    
    context = {
        'form': form,
        'title': '작품 등록',
    }
    return render(request, 'admin/artwork_form.html', context)

@login_required
def artwork_edit(request, pk):
    """작품 수정"""
    artwork = get_object_or_404(Artwork, pk=pk)
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            form.save()
            messages.success(request, f'작품 {artwork.title}이(가) 수정되었습니다.')
            return redirect('gallery:artwork_manage_list')
    else:
        form = ArtworkForm(instance=artwork)
    
    context = {
        'form': form,
        'title': f'작품 수정 - {artwork.title}',
        'artwork': artwork,
    }
    return render(request, 'admin/artwork_form.html', context)

@login_required
@require_POST
def artwork_delete(request, pk):
    """작품 삭제"""
    artwork = get_object_or_404(Artwork, pk=pk)
    title = artwork.title
    artwork.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': f'{title} 작품이 삭제되었습니다.'})
    
    messages.success(request, f'{title} 작품이 삭제되었습니다.')
    return redirect('gallery:artwork_manage_list')
