from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
import json
from .models import MenuItem

@staff_member_required
def menu_api_list(request):
    """메뉴 목록 API"""
    if request.method == 'GET':
        items = MenuItem.objects.all().order_by('order')
        data = [{
            'id': item.id,
            'title': item.title,
            'slug': item.slug,
            'menu_type': item.menu_type,
            'url': item.url,
            'order': item.order,
            'is_active': item.is_active,
            'is_visible': item.is_visible,
        } for item in items]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        item = MenuItem.objects.create(
            title=data['title'],
            slug=data['slug'],
            menu_type=data.get('menu_type', 'page'),
            url=data.get('url', ''),
            is_active=data.get('is_active', True),
            is_visible=data.get('is_visible', True),
            order=MenuItem.objects.count()
        )
        return JsonResponse({'id': item.id, 'success': True})

@staff_member_required
def menu_api_detail(request, pk):
    """메뉴 상세 API"""
    item = get_object_or_404(MenuItem, pk=pk)
    
    if request.method == 'GET':
        data = {
            'id': item.id,
            'title': item.title,
            'slug': item.slug,
            'menu_type': item.menu_type,
            'url': item.url,
            'order': item.order,
            'is_active': item.is_active,
            'is_visible': item.is_visible,
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        item.title = data.get('title', item.title)
        item.slug = data.get('slug', item.slug)
        item.menu_type = data.get('menu_type', item.menu_type)
        item.url = data.get('url', item.url)
        item.is_active = data.get('is_active', item.is_active)
        item.is_visible = data.get('is_visible', item.is_visible)
        item.save()
        return JsonResponse({'success': True})
    
    elif request.method == 'DELETE':
        item.delete()
        return JsonResponse({'success': True})

@staff_member_required
@csrf_exempt
def menu_toggle(request, pk):
    """메뉴 토글 API"""
    item = get_object_or_404(MenuItem, pk=pk)
    data = json.loads(request.body)
    item.is_visible = data.get('is_visible', item.is_visible)
    item.save()
    return JsonResponse({'success': True})

@staff_member_required
@csrf_exempt
def menu_reorder(request):
    """메뉴 순서 변경 API"""
    data = json.loads(request.body)
    for item_data in data['order']:
        MenuItem.objects.filter(id=item_data['id']).update(order=item_data['order'])
    return JsonResponse({'success': True})
