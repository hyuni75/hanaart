# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from apps.gallery.models import Artwork, History, About, HomeDesignType, Artist
from itertools import chain


def home(request):
    """홈 페이지 - 수억원급 프리미엄 디자인 3종 중 선택된 디자인 렌더링"""
    # 활성화된 작가 목록 가져오기
    active_artists = Artist.objects.filter(is_active=True).order_by('order')

    # 각 작가별로 최대 5개의 작품 가져오기 (is_featured=True, is_active=True)
    featured_artworks_list = []
    for artist in active_artists:
        artist_artworks = Artwork.objects.filter(
            artist=artist,
            is_featured=True,
            is_active=True
        ).order_by('order')[:5]  # 작가당 최대 5개

        featured_artworks_list.extend(artist_artworks)

    # 리스트를 QuerySet처럼 사용하기 위해 그대로 전달
    featured_artworks = featured_artworks_list

    # 현재 활성화된 홈 디자인 타입 가져오기
    active_design = HomeDesignType.get_active_design()

    # 디자인 타입에 따라 다른 템플릿 렌더링
    template_map = {
        'premium_grid': 'pages/home_premium_grid.html',
        'cube_3d': 'pages/home_cube_3d.html',
        'cinematic': 'pages/home_cinematic.html',
    }

    template_name = template_map.get(active_design, 'pages/home_premium_grid.html')

    return render(request, template_name, {
        'featured_artworks': featured_artworks
    })


def about(request):
    """인사말 페이지"""
    # 활성화된 인사말 데이터 가져오기 (첫 번째 항목)
    about_data = About.objects.filter(is_active=True).first()

    # 데이터가 없으면 기본값 사용
    if not about_data:
        about_data = {
            'title': '인사말',
            'content_1': '하나아트갤러리는 1990년 오픈하여 한국화랑협회 회원화랑으로 작가와 관람객이 예술로 교감하고 국내외 유망 신진작가를 발굴하고 중견, 원로작가까지 폭넓은 스펙트럼을 아우르며 회화, 조각, 설치, 전통미술 등 다양한 장르를 기획, 전시합니다.',
            'content_2': '또한 각종 국내, 외 아트페어와 해외교류전을 통해 한국미술의 가치를 널리 알리고 하나액자를 운영하여 작품보존과 미학적 완성도를 높이고 있다.',
            'content_3': '앞으로 예술과 삶을 잇는 다리로서 관람객에게 영감을 전하는 전시를 지속적으로 선보이겠습니다.',
        }

    return render(request, 'pages/about.html', {
        'about': about_data
    })


def history(request):
    """연혁 페이지 - 좌우 균형 분배"""
    histories = History.objects.filter(is_active=True).order_by('year', 'order')

    # 좌우 컬럼 분배 로직 (항목 개수 기준)
    total_count = histories.count()
    mid_point = total_count // 2

    left_histories = histories[:mid_point]
    right_histories = histories[mid_point:]

    return render(request, 'pages/history.html', {
        'left_histories': left_histories,
        'right_histories': right_histories
    })


def contact(request):
    """연락처 페이지"""
    return render(request, 'pages/contact.html')
