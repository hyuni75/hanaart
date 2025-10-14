# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from .models import Exhibition, ArtFair, Artist, Artwork, Frame


def exhibition_list(request):
    """전시 목록 페이지"""
    exhibitions = Exhibition.objects.filter(is_active=True)
    return render(request, 'gallery/exhibition_list.html', {'exhibitions': exhibitions})


def exhibition_detail(request, pk):
    """전시 상세 페이지"""
    exhibition = get_object_or_404(Exhibition, pk=pk, is_active=True)

    # 해당 작가의 모든 활성화된 작품 가져오기
    artworks = Artwork.objects.filter(
        artist=exhibition.artist,
        is_active=True
    ).order_by('order', '-created_at')

    return render(request, 'gallery/exhibition_detail.html', {
        'exhibition': exhibition,
        'artworks': artworks
    })


def artfair_list(request):
    """아트페어 페이지"""
    artfairs = ArtFair.objects.filter(is_active=True)
    return render(request, 'gallery/artfair_list.html', {'artfairs': artfairs})


def artist_list(request):
    """작가 페이지"""
    artists = Artist.objects.filter(is_active=True).prefetch_related('artworks')
    return render(request, 'gallery/artist_list.html', {'artists': artists})


def frame(request):
    """액자제작 페이지 - Frame 모델에서 데이터 가져오기"""
    frames = Frame.objects.filter(is_active=True).order_by('order')

    # 첫 번째 Frame 항목의 설명을 사용 (없으면 기본값)
    frame_info = frames.first()
    if not frame_info:
        description = "'하나액자'는 작품의 가치를 더욱 빛나게 하는 맞춤형 프레임을 제작합니다. 30년 전통과 현대적 감각을 담아 현대 공간에 어울리는 최적의 액자를 제안합니다."
    else:
        description = frame_info.description

    return render(request, 'gallery/frame.html', {
        'frames': frames,
        'description': description
    })
