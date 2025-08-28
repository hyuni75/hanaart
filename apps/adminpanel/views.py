from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from apps.gallery.models import Artist, Exhibition, Artwork

@login_required
def dashboard(request):
    """관리자 대시보드"""
    context = {
        "total_artists": Artist.objects.count(),
        "total_exhibitions": Exhibition.objects.count(), 
        "total_artworks": Artwork.objects.count(),
        "recent_artists": Artist.objects.order_by("-created_at")[:6],
        "recent_exhibitions": Exhibition.objects.order_by("-created_at")[:5],
        "current_exhibitions": Exhibition.objects.filter(is_current=True),
    }
    return render(request, "admin/gallery_dashboard.html", context)

@login_required
def redirect_to_artist_list(request):
    return redirect("gallery:artist_manage_list")

@login_required  
def redirect_to_exhibition_list(request):
    return redirect("gallery:exhibition_manage_list")
    
@login_required
def redirect_to_artwork_list(request):
    return redirect("gallery:artwork_manage_list")
