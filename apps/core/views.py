from django.shortcuts import render, redirect
from apps.navigator.models import MenuItem

def index(request):
    """메인 페이지"""
    from apps.gallery.models import Artist, Exhibition
    
    context = {
        'menu_items': MenuItem.objects.filter(is_active=True, is_visible=True, parent=None).order_by('order'),
        'artists': Artist.objects.filter(is_active=True).order_by('display_order', 'name')[:6],
        'current_exhibition': Exhibition.objects.filter(is_published=True).first(),
    }
    return render(request, 'core/index.html', context)

def dashboard(request):
    """관리자 대시보드"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin:login')
    
    context = {
        'menu_items': MenuItem.objects.all().order_by('order'),
        'total_menu_items': MenuItem.objects.count(),
        'active_menu_items': MenuItem.objects.filter(is_active=True).count(),
    }
    return render(request, 'admin/dashboard.html', context)
