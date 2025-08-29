def menu_items(request):
    """전역 메뉴 아이템 (navigator 앱 삭제로 인해 비활성화)"""
    return {
        'menu_items': []
    }