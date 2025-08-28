from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from .models import Page, Block, Template
from apps.interaction.models import Comment, Like, View as PageView
from apps.moderation.models import ContentFilter

class PageDetailView(DetailView):
    model = Page
    template_name = 'pagebuilder/page_detail.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_object(self):
        obj = super().get_object()
        if not obj.is_published:
            raise Http404("페이지를 찾을 수 없습니다.")
        
        # 조회수 증가
        if self.request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(Page)
            PageView.objects.get_or_create(
                content_type=content_type,
                object_id=obj.id,
                user=self.request.user,
                defaults={'ip_address': self.get_client_ip()}
            )
        return obj
    
    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.object
        
        # 블록 가져오기
        context['blocks'] = page.blocks.filter(is_visible=True).order_by('order')
        
        # 템플릿 정보
        if page.template:
            context['custom_template'] = page.template.html_template
            context['custom_styles'] = page.template.css_styles
        
        # 상호작용 통계
        content_type = ContentType.objects.get_for_model(Page)
        
        # 댓글
        if page.enable_comments:
            comments = Comment.objects.filter(
                content_type=content_type,
                object_id=page.id,
                is_approved=True,
                is_deleted=False,
                parent=None
            ).order_by('-created_at')
            
            # 댓글 필터링
            filtered_comments = []
            for comment in comments:
                is_clean, filtered_text, _, _ = ContentFilter.check(comment.content)
                if is_clean or comment.is_filtered:
                    comment.display_content = filtered_text if not is_clean else comment.content
                    filtered_comments.append(comment)
            
            context['comments'] = filtered_comments
            context['comment_count'] = len(filtered_comments)
        
        # 좋아요
        if page.enable_likes:
            context['like_count'] = Like.objects.filter(
                content_type=content_type,
                object_id=page.id
            ).count()
            
            if self.request.user.is_authenticated:
                context['user_liked'] = Like.objects.filter(
                    content_type=content_type,
                    object_id=page.id,
                    user=self.request.user
                ).exists()
        
        # 조회수
        context['view_count'] = PageView.objects.filter(
            content_type=content_type,
            object_id=page.id
        ).count()
        
        return context

class PageListView(ListView):
    model = Page
    template_name = 'pagebuilder/page_list.html'
    context_object_name = 'pages'
    paginate_by = 12
    
    def get_queryset(self):
        return Page.objects.filter(is_published=True).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 각 페이지의 통계 추가
        for page in context['pages']:
            content_type = ContentType.objects.get_for_model(Page)
            
            # 조회수
            page.view_count = PageView.objects.filter(
                content_type=content_type,
                object_id=page.id
            ).count()
            
            # 댓글 수
            if page.enable_comments:
                page.comment_count = Comment.objects.filter(
                    content_type=content_type,
                    object_id=page.id,
                    is_approved=True,
                    is_deleted=False
                ).count()
            
            # 좋아요 수
            if page.enable_likes:
                page.like_count = Like.objects.filter(
                    content_type=content_type,
                    object_id=page.id
                ).count()
        
        return context

# AJAX 뷰
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json

@require_POST
@login_required
def toggle_like(request, page_id):
    """페이지 좋아요 토글"""
    page = get_object_or_404(Page, id=page_id, is_published=True)
    
    if not page.enable_likes:
        return JsonResponse({'error': '이 페이지는 좋아요를 받을 수 없습니다.'}, status=400)
    
    content_type = ContentType.objects.get_for_model(Page)
    like, created = Like.objects.get_or_create(
        content_type=content_type,
        object_id=page.id,
        user=request.user,
        defaults={'ip_address': request.META.get('REMOTE_ADDR')}
    )
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    like_count = Like.objects.filter(
        content_type=content_type,
        object_id=page.id
    ).count()
    
    return JsonResponse({
        'liked': liked,
        'like_count': like_count
    })

@require_POST
def add_comment(request, page_id):
    """페이지에 댓글 추가"""
    page = get_object_or_404(Page, id=page_id, is_published=True)
    
    if not page.enable_comments:
        return JsonResponse({'error': '이 페이지는 댓글을 받을 수 없습니다.'}, status=400)
    
    data = json.loads(request.body)
    content = data.get('content', '').strip()
    
    if not content:
        return JsonResponse({'error': '댓글 내용을 입력해주세요.'}, status=400)
    
    # 콘텐츠 필터링
    is_clean, filtered_text, matched_rules, action = ContentFilter.check(content)
    
    if action == 'block':
        return JsonResponse({'error': '부적절한 내용이 포함되어 있습니다.'}, status=400)
    
    content_type = ContentType.objects.get_for_model(Page)
    
    comment = Comment.objects.create(
        content_type=content_type,
        object_id=page.id,
        content=content,
        author=request.user if request.user.is_authenticated else None,
        author_name=data.get('author_name', '') if not request.user.is_authenticated else '',
        author_email=data.get('author_email', '') if not request.user.is_authenticated else '',
        is_approved=is_clean,  # 깨끗한 댓글만 자동 승인
        is_filtered=not is_clean,
        filtered_reason=', '.join(matched_rules) if matched_rules else '',
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    if comment.is_approved:
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': filtered_text if not is_clean else comment.content,
                'author': comment.author.username if comment.author else comment.author_name,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                'is_filtered': comment.is_filtered
            }
        })
    else:
        return JsonResponse({
            'success': True,
            'pending': True,
            'message': '댓글이 검토 후 게시됩니다.'
        })