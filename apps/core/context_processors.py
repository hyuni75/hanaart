from apps.navigator.models import MenuItem

def menu_items(request):
    """전역 메뉴 아이템"""
    return {
        'menu_items': MenuItem.objects.filter(
            is_active=True, 
            is_visible=True, 
            parent=None
        ).order_by('order')
    }