# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from apps.gallery.models import History, ArtFair, Artist, Artwork, Exhibition, About, Frame, Contact, HomeDesignType


def login_view(request):
    """관리자 로그인 페이지 및 처리"""
    if request.user.is_authenticated:
        return redirect('admin_panel:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get('next', 'admin_panel:index')
            return redirect(next_url)
        else:
            return render(request, 'admin_panel/login.html', {
                'error': '사용자명 또는 비밀번호가 올바르지 않습니다.'
            })

    return render(request, 'admin_panel/login.html')


def logout_view(request):
    """관리자 로그아웃 처리"""
    auth_logout(request)
    return redirect('admin_panel:login')


@login_required
def index(request):
    """관리자 메인 대시보드"""
    return render(request, 'admin_panel/index.html')


@login_required
def template_manage(request):
    """템플릿 섹션 관리"""
    return render(request, 'admin_panel/template_manage.html')


@login_required
def artist_manage(request):
    """작가 관리"""
    return render(request, 'admin_panel/artist_manage.html')


@login_required
def artwork_manage(request):
    """작품 관리"""
    return render(request, 'admin_panel/artwork_manage.html')


@login_required
def exhibition_manage(request):
    """전시 관리"""
    return render(request, 'admin_panel/exhibition_manage.html')


@login_required
def artfair_manage(request):
    """아트페어 관리"""
    return render(request, 'admin_panel/artfair_manage.html')


@login_required
def history_manage(request):
    """연혁 관리"""
    return render(request, 'admin_panel/history_manage.html')


@login_required
def about_manage(request):
    """인사말 관리"""
    return render(request, 'admin_panel/about_manage.html')


@login_required
def frame_manage(request):
    """액자 관리"""
    return render(request, 'admin_panel/frame_manage.html')


@login_required
def contact_manage(request):
    """연락처 관리"""
    return render(request, 'admin_panel/contact_manage.html')


@login_required
def statistics_api(request):
    """대시보드 통계 API"""
    data = {
        'history_count': History.objects.filter(is_active=True).count(),
        'artfair_count': ArtFair.objects.filter(is_active=True).count(),
        'artist_count': Artist.objects.filter(is_active=True).count(),
        'artwork_count': Artwork.objects.filter(is_active=True).count(),
        'exhibition_count': Exhibition.objects.filter(is_active=True).count(),
    }
    return JsonResponse(data)


# ===================== 연혁 API =====================

@login_required
def history_list_api(request):
    """연혁 목록 API"""
    histories = History.objects.all().order_by('order', 'year')
    data = {
        'histories': [{
            'id': h.id,
            'year': h.year,
            'content': h.content,
            'order': h.order,
            'is_active': h.is_active,
        } for h in histories]
    }
    return JsonResponse(data)


@login_required
def history_detail_api(request, pk):
    """연혁 상세 API"""
    history = get_object_or_404(History, pk=pk)
    data = {
        'id': history.id,
        'year': history.year,
        'content': history.content,
        'order': history.order,
        'is_active': history.is_active,
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def history_create_api(request):
    """연혁 생성 API"""
    try:
        data = json.loads(request.body)
        history = History.objects.create(
            year=data['year'],
            content=data['content'],
            order=data['order'],
            is_active=data.get('is_active', True)
        )
        return JsonResponse({
            'success': True,
            'message': '연혁이 추가되었습니다.',
            'id': history.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["PUT"])
def history_update_api(request, pk):
    """연혁 수정 API"""
    try:
        history = get_object_or_404(History, pk=pk)
        data = json.loads(request.body)

        history.year = data['year']
        history.content = data['content']
        history.order = data['order']
        history.is_active = data.get('is_active', True)
        history.save()

        return JsonResponse({
            'success': True,
            'message': '연혁이 수정되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["DELETE"])
def history_delete_api(request, pk):
    """연혁 삭제 API"""
    try:
        history = get_object_or_404(History, pk=pk)
        history.delete()
        return JsonResponse({
            'success': True,
            'message': '연혁이 삭제되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


# ===================== 아트페어 API =====================

@login_required
def artfair_list_api(request):
    """아트페어 목록 API"""
    artfairs = ArtFair.objects.all().order_by('-year')
    data = {
        'artfairs': [{
            'id': af.id,
            'year': af.year,
            'title': af.title,
            'description': af.description,
            'image': af.image.url if af.image else None,
            'is_active': af.is_active,
        } for af in artfairs]
    }
    return JsonResponse(data)


@login_required
def artfair_detail_api(request, pk):
    """아트페어 상세 API"""
    artfair = get_object_or_404(ArtFair, pk=pk)
    data = {
        'id': artfair.id,
        'year': artfair.year,
        'title': artfair.title,
        'description': artfair.description,
        'image': artfair.image.url if artfair.image else None,
        'is_active': artfair.is_active,
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def artfair_create_api(request):
    """아트페어 생성 API"""
    try:
        artfair = ArtFair.objects.create(
            year=request.POST['year'],
            title=request.POST['title'],
            description=request.POST.get('description', ''),
            is_active=request.POST.get('is_active', 'true').lower() == 'true'
        )

        # 이미지 파일 처리
        if 'image' in request.FILES:
            artfair.image = request.FILES['image']
            artfair.save()

        return JsonResponse({
            'success': True,
            'message': '아트페어가 추가되었습니다.',
            'id': artfair.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def artfair_update_api(request, pk):
    """아트페어 수정 API"""
    try:
        artfair = get_object_or_404(ArtFair, pk=pk)

        artfair.year = request.POST['year']
        artfair.title = request.POST['title']
        artfair.description = request.POST.get('description', '')
        artfair.is_active = request.POST.get('is_active', 'true').lower() == 'true'

        # 이미지 파일 처리
        if 'image' in request.FILES:
            artfair.image = request.FILES['image']

        artfair.save()

        return JsonResponse({
            'success': True,
            'message': '아트페어가 수정되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def artfair_delete_api(request, pk):
    """아트페어 삭제 API"""
    try:
        artfair = get_object_or_404(ArtFair, pk=pk)
        artfair.delete()
        return JsonResponse({
            'success': True,
            'message': '아트페어가 삭제되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


# ===================== 작가 API =====================

@login_required
def artist_list_api(request):
    """작가 목록 API"""
    artists = Artist.objects.all().order_by('order', 'name')
    data = {
        'artists': [{
            'id': artist.id,
            'name': artist.name,
            'name_en': artist.name_en,
            'description': artist.description,
            'profile_image': artist.profile_image.url if artist.profile_image else None,
            'order': artist.order,
            'is_active': artist.is_active,
        } for artist in artists]
    }
    return JsonResponse(data)


@login_required
def artist_detail_api(request, pk):
    """작가 상세 API"""
    artist = get_object_or_404(Artist, pk=pk)
    data = {
        'id': artist.id,
        'name': artist.name,
        'name_en': artist.name_en,
        'description': artist.description,
        'profile_image': artist.profile_image.url if artist.profile_image else None,
        'order': artist.order,
        'is_active': artist.is_active,
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def artist_create_api(request):
    """작가 생성 API"""
    try:
        artist = Artist.objects.create(
            name=request.POST['name'],
            name_en=request.POST.get('name_en', ''),
            description=request.POST['description'],
            order=request.POST.get('order', 0),
            is_active=request.POST.get('is_active', 'true').lower() == 'true'
        )

        # 이미지 파일 처리
        if 'profile_image' in request.FILES:
            artist.profile_image = request.FILES['profile_image']
            artist.save()

        return JsonResponse({
            'success': True,
            'message': '작가가 추가되었습니다.',
            'id': artist.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def artist_update_api(request, pk):
    """작가 수정 API"""
    try:
        artist = get_object_or_404(Artist, pk=pk)

        artist.name = request.POST['name']
        artist.name_en = request.POST.get('name_en', '')
        artist.description = request.POST['description']
        artist.order = request.POST.get('order', 0)
        artist.is_active = request.POST.get('is_active', 'true').lower() == 'true'

        # 이미지 파일 처리
        if 'profile_image' in request.FILES:
            artist.profile_image = request.FILES['profile_image']

        artist.save()

        return JsonResponse({
            'success': True,
            'message': '작가가 수정되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def artist_delete_api(request, pk):
    """작가 삭제 API"""
    try:
        artist = get_object_or_404(Artist, pk=pk)
        artist.delete()
        return JsonResponse({
            'success': True,
            'message': '작가가 삭제되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


# ===================== 작품 API =====================

@login_required
def artwork_list_api(request):
    """작품 목록 API"""
    artworks = Artwork.objects.select_related('artist').all().order_by('order', '-created_at')
    data = {
        'artworks': [{
            'id': artwork.id,
            'artist_id': artwork.artist.id,
            'artist_name': artwork.artist.name,
            'title': artwork.title,
            'title_en': artwork.title_en,
            'description': artwork.description,
            'image': artwork.image.url if artwork.image else None,
            'year': artwork.year,
            'size': artwork.size,
            'material': artwork.material,
            'order': artwork.order,
            'is_featured': artwork.is_featured,
            'is_active': artwork.is_active,
        } for artwork in artworks]
    }
    return JsonResponse(data)


@login_required
def artwork_detail_api(request, pk):
    """작품 상세 API"""
    artwork = get_object_or_404(Artwork.objects.select_related('artist'), pk=pk)
    data = {
        'id': artwork.id,
        'artist_id': artwork.artist.id,
        'artist_name': artwork.artist.name,
        'title': artwork.title,
        'title_en': artwork.title_en,
        'description': artwork.description,
        'image': artwork.image.url if artwork.image else None,
        'year': artwork.year,
        'size': artwork.size,
        'material': artwork.material,
        'order': artwork.order,
        'is_featured': artwork.is_featured,
        'is_active': artwork.is_active,
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def artwork_create_api(request):
    """작품 생성 API"""
    try:
        artwork = Artwork.objects.create(
            artist_id=request.POST['artist_id'],
            title=request.POST['title'],
            title_en=request.POST.get('title_en', ''),
            description=request.POST.get('description', ''),
            year=request.POST.get('year') if request.POST.get('year') else None,
            size=request.POST.get('size', ''),
            material=request.POST.get('material', ''),
            order=request.POST.get('order', 0),
            is_featured=request.POST.get('is_featured', 'false').lower() == 'true',
            is_active=request.POST.get('is_active', 'true').lower() == 'true'
        )

        # 이미지 파일 처리
        if 'image' in request.FILES:
            artwork.image = request.FILES['image']
            artwork.save()

        return JsonResponse({
            'success': True,
            'message': '작품이 추가되었습니다.',
            'id': artwork.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def artwork_update_api(request, pk):
    """작품 수정 API"""
    try:
        artwork = get_object_or_404(Artwork, pk=pk)

        artwork.artist_id = request.POST['artist_id']
        artwork.title = request.POST['title']
        artwork.title_en = request.POST.get('title_en', '')
        artwork.description = request.POST.get('description', '')
        artwork.year = request.POST.get('year') if request.POST.get('year') else None
        artwork.size = request.POST.get('size', '')
        artwork.material = request.POST.get('material', '')
        artwork.order = request.POST.get('order', 0)
        artwork.is_featured = request.POST.get('is_featured', 'false').lower() == 'true'
        artwork.is_active = request.POST.get('is_active', 'true').lower() == 'true'

        # 이미지 파일 처리
        if 'image' in request.FILES:
            artwork.image = request.FILES['image']

        artwork.save()

        return JsonResponse({
            'success': True,
            'message': '작품이 수정되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def artwork_delete_api(request, pk):
    """작품 삭제 API"""
    try:
        artwork = get_object_or_404(Artwork, pk=pk)
        artwork.delete()
        return JsonResponse({
            'success': True,
            'message': '작품이 삭제되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


# ===================== 전시 API =====================

@login_required
def exhibition_list_api(request):
    """전시 목록 API"""
    exhibitions = Exhibition.objects.select_related('artist').all().order_by('order', '-start_date')
    data = {
        'exhibitions': [{
            'id': exhibition.id,
            'artist_id': exhibition.artist.id,
            'artist': exhibition.artist.name,
            'title': exhibition.title,
            'title_en': exhibition.title_en,
            'description': exhibition.description,
            'location': exhibition.location,
            'start_date': exhibition.start_date.strftime('%Y-%m-%d'),
            'end_date': exhibition.end_date.strftime('%Y-%m-%d'),
            'poster_image': exhibition.poster_image.url if exhibition.poster_image else None,
            'order': exhibition.order,
            'is_ongoing': exhibition.is_ongoing,
            'is_active': exhibition.is_active,
        } for exhibition in exhibitions]
    }
    return JsonResponse(data)


@login_required
def exhibition_detail_api(request, pk):
    """전시 상세 API"""
    exhibition = get_object_or_404(Exhibition.objects.select_related('artist'), pk=pk)
    data = {
        'id': exhibition.id,
        'artist_id': exhibition.artist.id,
        'artist_name': exhibition.artist.name,
        'title': exhibition.title,
        'title_en': exhibition.title_en,
        'description': exhibition.description,
        'location': exhibition.location,
        'start_date': exhibition.start_date.strftime('%Y-%m-%d'),
        'end_date': exhibition.end_date.strftime('%Y-%m-%d'),
        'poster_image': exhibition.poster_image.url if exhibition.poster_image else None,
        'order': exhibition.order,
        'is_ongoing': exhibition.is_ongoing,
        'is_active': exhibition.is_active,
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def exhibition_create_api(request):
    """전시 생성 API"""
    try:
        exhibition = Exhibition.objects.create(
            artist_id=request.POST['artist_id'],
            title=request.POST['title'],
            title_en=request.POST.get('title_en', ''),
            description=request.POST['description'],
            location=request.POST.get('location', ''),
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            order=request.POST.get('order', 0),
            is_active=request.POST.get('is_active', 'true').lower() == 'true'
        )

        # 이미지 파일 처리
        if 'poster_image' in request.FILES:
            exhibition.poster_image = request.FILES['poster_image']
            exhibition.save()

        return JsonResponse({
            'success': True,
            'message': '전시가 추가되었습니다.',
            'id': exhibition.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def exhibition_update_api(request, pk):
    """전시 수정 API"""
    try:
        exhibition = get_object_or_404(Exhibition, pk=pk)

        exhibition.artist_id = request.POST['artist_id']
        exhibition.title = request.POST['title']
        exhibition.title_en = request.POST.get('title_en', '')
        exhibition.description = request.POST['description']
        exhibition.location = request.POST.get('location', '')
        exhibition.start_date = request.POST['start_date']
        exhibition.end_date = request.POST['end_date']
        exhibition.order = request.POST.get('order', 0)
        exhibition.is_active = request.POST.get('is_active', 'true').lower() == 'true'

        # 이미지 파일 처리
        if 'poster_image' in request.FILES:
            exhibition.poster_image = request.FILES['poster_image']

        exhibition.save()

        return JsonResponse({
            'success': True,
            'message': '전시가 수정되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def exhibition_delete_api(request, pk):
    """전시 삭제 API"""
    try:
        exhibition = get_object_or_404(Exhibition, pk=pk)
        exhibition.delete()
        return JsonResponse({
            'success': True,
            'message': '전시가 삭제되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


# ===================== 인사말 API =====================

@login_required
def about_list_api(request):
    """인사말 목록 API"""
    abouts = About.objects.all()
    data = {
        'abouts': [{
            'id': about.id,
            'title': about.title,
            'content_1': about.content_1,
            'content_2': about.content_2,
            'content_3': about.content_3,
            'image_1': about.image_1.url if about.image_1 else None,
            'image_1_title': about.image_1_title,
            'image_1_desc': about.image_1_desc,
            'image_2': about.image_2.url if about.image_2 else None,
            'image_2_title': about.image_2_title,
            'image_2_desc': about.image_2_desc,
            'is_active': about.is_active,
        } for about in abouts]
    }
    return JsonResponse(data)


@login_required
def about_detail_api(request, pk):
    """인사말 상세 API"""
    about = get_object_or_404(About, pk=pk)
    data = {
        'id': about.id,
        'title': about.title,
        'content_1': about.content_1,
        'content_2': about.content_2,
        'content_3': about.content_3,
        'image_1': about.image_1.url if about.image_1 else None,
        'image_1_title': about.image_1_title,
        'image_1_desc': about.image_1_desc,
        'image_2': about.image_2.url if about.image_2 else None,
        'image_2_title': about.image_2_title,
        'image_2_desc': about.image_2_desc,
        'is_active': about.is_active,
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def about_create_api(request):
    """인사말 생성 API"""
    try:
        about = About.objects.create(
            title=request.POST['title'],
            content_1=request.POST['content_1'],
            content_2=request.POST['content_2'],
            content_3=request.POST['content_3'],
            image_1_title=request.POST.get('image_1_title', '전시장 내부'),
            image_1_desc=request.POST.get('image_1_desc', '하나아트갤러리 전시 공간'),
            image_2_title=request.POST.get('image_2_title', '전시장 도면'),
            image_2_desc=request.POST.get('image_2_desc', '갤러리 평면도'),
            is_active=request.POST.get('is_active', 'true').lower() == 'true'
        )

        # 이미지 파일 처리
        if 'image_1' in request.FILES:
            about.image_1 = request.FILES['image_1']
        if 'image_2' in request.FILES:
            about.image_2 = request.FILES['image_2']

        about.save()

        return JsonResponse({
            'success': True,
            'message': '인사말이 추가되었습니다.',
            'id': about.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def about_update_api(request, pk):
    """인사말 수정 API"""
    try:
        about = get_object_or_404(About, pk=pk)

        about.title = request.POST['title']
        about.content_1 = request.POST['content_1']
        about.content_2 = request.POST['content_2']
        about.content_3 = request.POST['content_3']
        about.image_1_title = request.POST.get('image_1_title', '전시장 내부')
        about.image_1_desc = request.POST.get('image_1_desc', '하나아트갤러리 전시 공간')
        about.image_2_title = request.POST.get('image_2_title', '전시장 도면')
        about.image_2_desc = request.POST.get('image_2_desc', '갤러리 평면도')
        about.is_active = request.POST.get('is_active', 'true').lower() == 'true'

        # 이미지 파일 처리
        if 'image_1' in request.FILES:
            about.image_1 = request.FILES['image_1']
        if 'image_2' in request.FILES:
            about.image_2 = request.FILES['image_2']

        about.save()

        return JsonResponse({
            'success': True,
            'message': '인사말이 수정되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def about_delete_api(request, pk):
    """인사말 삭제 API"""
    try:
        about = get_object_or_404(About, pk=pk)
        about.delete()
        return JsonResponse({
            'success': True,
            'message': '인사말이 삭제되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


# ===================== 액자 API =====================

@login_required
def frame_list_api(request):
    """액자 목록 API"""
    frames = Frame.objects.all().order_by('order')
    data = {
        'frames': [{
            'id': frame.id,
            'title': frame.title,
            'description': frame.description,
            'image_1': frame.image_1.url if frame.image_1 else None,
            'image_2': frame.image_2.url if frame.image_2 else None,
            'image_3': frame.image_3.url if frame.image_3 else None,
            'order': frame.order,
            'is_active': frame.is_active,
        } for frame in frames]
    }
    return JsonResponse(data)


@login_required
def frame_detail_api(request, pk):
    """액자 상세 API"""
    frame = get_object_or_404(Frame, pk=pk)
    data = {
        'id': frame.id,
        'title': frame.title,
        'description': frame.description,
        'image_1': frame.image_1.url if frame.image_1 else None,
        'image_2': frame.image_2.url if frame.image_2 else None,
        'image_3': frame.image_3.url if frame.image_3 else None,
        'order': frame.order,
        'is_active': frame.is_active,
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def frame_create_api(request):
    """액자 생성 API"""
    try:
        frame = Frame.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            order=request.POST.get('order', 0),
            is_active=request.POST.get('is_active', 'true').lower() == 'true'
        )

        # 이미지 파일 처리 (3개)
        if 'image_1' in request.FILES:
            frame.image_1 = request.FILES['image_1']
        if 'image_2' in request.FILES:
            frame.image_2 = request.FILES['image_2']
        if 'image_3' in request.FILES:
            frame.image_3 = request.FILES['image_3']

        frame.save()

        return JsonResponse({
            'success': True,
            'message': '액자가 추가되었습니다.',
            'id': frame.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def frame_update_api(request, pk):
    """액자 수정 API"""
    try:
        frame = get_object_or_404(Frame, pk=pk)

        frame.title = request.POST['title']
        frame.description = request.POST['description']
        frame.order = request.POST.get('order', 0)
        frame.is_active = request.POST.get('is_active', 'true').lower() == 'true'

        # 이미지 파일 처리 (3개)
        if 'image_1' in request.FILES:
            frame.image_1 = request.FILES['image_1']
        if 'image_2' in request.FILES:
            frame.image_2 = request.FILES['image_2']
        if 'image_3' in request.FILES:
            frame.image_3 = request.FILES['image_3']

        frame.save()

        return JsonResponse({
            'success': True,
            'message': '액자가 수정되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def frame_delete_api(request, pk):
    """액자 삭제 API"""
    try:
        frame = get_object_or_404(Frame, pk=pk)
        frame.delete()
        return JsonResponse({
            'success': True,
            'message': '액자가 삭제되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


# ===================== 연락처 API =====================

@login_required
def contact_list_api(request):
    """연락처 목록 API"""
    contacts = Contact.objects.all()
    data = {
        'contacts': [{
            'id': contact.id,
            'title': contact.title,
            'ceo_name': contact.ceo_name,
            'ceo_name_en': contact.ceo_name_en,
            'phone': contact.phone,
            'fax': contact.fax,
            'mobile': contact.mobile,
            'email': contact.email,
            'address': contact.address,
            'address_en': contact.address_en,
            'is_active': contact.is_active,
        } for contact in contacts]
    }
    return JsonResponse(data)


@login_required
def contact_detail_api(request, pk):
    """연락처 상세 API"""
    contact = get_object_or_404(Contact, pk=pk)
    data = {
        'id': contact.id,
        'title': contact.title,
        'ceo_name': contact.ceo_name,
        'ceo_name_en': contact.ceo_name_en,
        'phone': contact.phone,
        'fax': contact.fax,
        'mobile': contact.mobile,
        'email': contact.email,
        'address': contact.address,
        'address_en': contact.address_en,
        'is_active': contact.is_active,
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def contact_create_api(request):
    """연락처 생성 API"""
    try:
        contact = Contact.objects.create(
            title=request.POST['title'],
            ceo_name=request.POST['ceo_name'],
            ceo_name_en=request.POST.get('ceo_name_en', ''),
            phone=request.POST['phone'],
            fax=request.POST.get('fax', ''),
            mobile=request.POST.get('mobile', ''),
            email=request.POST['email'],
            address=request.POST['address'],
            address_en=request.POST.get('address_en', ''),
            is_active=request.POST.get('is_active', 'true').lower() == 'true'
        )

        return JsonResponse({
            'success': True,
            'message': '연락처가 추가되었습니다.',
            'id': contact.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def contact_update_api(request, pk):
    """연락처 수정 API"""
    try:
        contact = get_object_or_404(Contact, pk=pk)

        contact.title = request.POST['title']
        contact.ceo_name = request.POST['ceo_name']
        contact.ceo_name_en = request.POST.get('ceo_name_en', '')
        contact.phone = request.POST['phone']
        contact.fax = request.POST.get('fax', '')
        contact.mobile = request.POST.get('mobile', '')
        contact.email = request.POST['email']
        contact.address = request.POST['address']
        contact.address_en = request.POST.get('address_en', '')
        contact.is_active = request.POST.get('is_active', 'true').lower() == 'true'

        contact.save()

        return JsonResponse({
            'success': True,
            'message': '연락처가 수정되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def contact_delete_api(request, pk):
    """연락처 삭제 API"""
    try:
        contact = get_object_or_404(Contact, pk=pk)
        contact.delete()
        return JsonResponse({
            'success': True,
            'message': '연락처가 삭제되었습니다.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


# ===================== 홈 디자인 관리 =====================

@login_required
def home_design_manage(request):
    """홈 디자인 관리 페이지"""
    return render(request, 'admin_panel/home_design_manage.html')


@login_required
def home_design_current_api(request):
    """현재 활성화된 홈 디자인 타입 조회 API"""
    design = HomeDesignType.objects.filter(is_active=True).first()

    if not design:
        # 기본 레코드 생성
        design = HomeDesignType.objects.create(
            design_type='premium_grid',
            is_active=True,
            updated_by=request.user.username
        )

    data = {
        'id': design.id,
        'design_type': design.design_type,
        'design_name': design.get_design_type_display(),
        'is_active': design.is_active,
        'updated_at': design.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_by': design.updated_by,
        'designs': [
            {
                'value': 'premium_grid',
                'name': '프리미엄 그리드 모자이크 (GSAP + Lenis + GLSL Shaders)',
                'description': '비대칭 그리드 레이아웃, 스무스 스크롤, 프리미엄 인터랙션',
                'preview': '/static/images/preview_premium_grid.jpg'
            },
            {
                'value': 'cube_3d',
                'name': '3D 큐브 갤러리 (Three.js + WebGL)',
                'description': '3D 공간의 작품 큐브, 마우스 드래그 회전, WebGL 렌더링',
                'preview': '/static/images/preview_cube_3d.jpg'
            },
            {
                'value': 'cinematic',
                'name': '시네마틱 풀스크린 슬라이더 (영화급 트랜지션)',
                'description': '영화 같은 풀스크린 슬라이더, 시네마틱 타이포그래피, 자동재생',
                'preview': '/static/images/preview_cinematic.jpg'
            }
        ]
    }
    return JsonResponse(data)


@login_required
@require_http_methods(["POST"])
def home_design_switch_api(request):
    """홈 디자인 타입 변경 API"""
    try:
        data = json.loads(request.body)
        design_type = data.get('design_type')

        if not design_type:
            return JsonResponse({
                'success': False,
                'message': '디자인 타입을 선택해주세요.'
            }, status=400)

        # 유효한 디자인 타입인지 확인
        valid_types = ['premium_grid', 'cube_3d', 'cinematic']
        if design_type not in valid_types:
            return JsonResponse({
                'success': False,
                'message': '유효하지 않은 디자인 타입입니다.'
            }, status=400)

        # 현재 활성화된 디자인 가져오기
        current_design = HomeDesignType.objects.filter(is_active=True).first()

        if current_design and current_design.design_type == design_type:
            return JsonResponse({
                'success': True,
                'message': '이미 선택된 디자인입니다.',
                'design_name': current_design.get_design_type_display()
            })

        # 모든 디자인 비활성화
        HomeDesignType.objects.update(is_active=False)

        # 새 디자인 활성화 (또는 생성)
        design, created = HomeDesignType.objects.get_or_create(
            design_type=design_type,
            defaults={
                'is_active': True,
                'updated_by': request.user.username
            }
        )

        if not created:
            design.is_active = True
            design.updated_by = request.user.username
            design.save()

        return JsonResponse({
            'success': True,
            'message': f'홈 디자인이 "{design.get_design_type_display()}"(으)로 변경되었습니다.',
            'design_type': design.design_type,
            'design_name': design.get_design_type_display()
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)
