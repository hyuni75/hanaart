from django.shortcuts import render, redirect

def index(request):
    """메인 페이지"""
    # 새로운 하나아트갤러리 메인 페이지 템플릿 렌더링
    return render(request, 'index_new.html')

def about(request):
    """소개·인사말 페이지"""
    return render(request, 'about.html')

def history(request):
    """연혁 페이지"""
    return render(request, 'history.html')

def exhibition(request):
    """현재전시 페이지"""
    from apps.gallery.models import CurrentExhibition
    exhibition = CurrentExhibition.objects.filter(is_active=True).first()
    return render(request, 'exhibition.html', {'exhibition': exhibition})

def artfair(request):
    """아트페어 페이지"""
    return render(request, 'artfair.html')

def artists(request):
    """전속작가 페이지"""
    from apps.gallery.models import SimpleArtist
    artists = SimpleArtist.objects.filter(is_active=True).order_by('display_order', 'name')
    return render(request, 'artists.html', {'artists': artists})

def frame(request):
    """액자제작 페이지"""
    return render(request, 'frame.html')

def location(request):
    """찾아오는 길 페이지"""
    return render(request, 'location.html')

def contact(request):
    """연락처 페이지"""
    return render(request, 'contact.html')

def dashboard(request):
    """관리자 대시보드 (gallery 앱으로 이동)"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin:login')
    
    return redirect('gallery:admin_dashboard')
