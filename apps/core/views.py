from django.shortcuts import render, redirect

def index(request):
    """메인 페이지"""
    from apps.gallery.models import Artist, Exhibition, Artwork
    from django.urls import reverse
    
    # 현재 전시 가져오기
    current_exhibitions = Exhibition.objects.filter(
        is_current=True, 
        is_published=True
    )
    
    # 전시 링크 로직: 1개면 직접 링크, 여러개면 목록 페이지
    exhibition_link = None
    if current_exhibitions.count() == 1:
        exhibition = current_exhibitions.first()
        exhibition_link = reverse('gallery:exhibition_detail', kwargs={'slug': exhibition.slug})
    elif current_exhibitions.count() > 1:
        exhibition_link = reverse('gallery:exhibition_list')
    
    # 최신 작품 가져오기 (히어로 섹션 로테이션용)
    all_artworks = Artwork.objects.filter(
        is_published=True
    ).select_related('artist').order_by('-created_at')[:10]
    
    # 전속 작가와 일반 작가 분리
    exclusive_artists = Artist.objects.filter(
        is_active=True, 
        is_exclusive=True
    ).prefetch_related('artworks').order_by('display_order', 'name')
    
    regular_artists = Artist.objects.filter(
        is_active=True, 
        is_exclusive=False
    ).prefetch_related('artworks').order_by('display_order', 'name')
    
    context = {
        'current_exhibition': current_exhibitions.first() if current_exhibitions.exists() else None,
        'exhibition_link': exhibition_link,
        'all_artworks': all_artworks,
        'exclusive_artists': exclusive_artists,
        'regular_artists': regular_artists,
        'artists': Artist.objects.filter(is_active=True).prefetch_related('artworks').order_by('display_order', 'name')[:6],
    }
    return render(request, 'core/index.html', context)

def dashboard(request):
    """관리자 대시보드 (gallery 앱으로 이동)"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin:login')
    
    return redirect('gallery:admin_dashboard')
