from django import forms
from .models import Artist, Exhibition, Artwork

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = [
            'name', 'name_en', 'birth_year', 
            'profile_image', 'bio', 'education', 'awards',
            'email', 'phone', 'website', 'instagram',
            'is_exclusive', 'is_active', 'display_order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '작가명'}),
            'name_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '영문명'}),
            'birth_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '출생년도'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '작가 소개'}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '학력'}),
            'awards': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '수상경력'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '전화번호'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': '웹사이트'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@instagram'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '표시 순서'}),
            'is_exclusive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ExhibitionForm(forms.ModelForm):
    # 작품 선택을 위한 추가 필드
    artworks = forms.ModelMultipleChoiceField(
        queryset=Artwork.objects.filter(is_published=True).select_related('artist'),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 10}),
        required=False,
        label='전시 작품'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 작품 선택 필드의 표시 형식 개선
        self.fields['artworks'].label_from_instance = lambda obj: f"{obj.artist.name} - {obj.title}"
        # 작가 선택 필드의 표시 형식 개선
        self.fields['artists'].label_from_instance = lambda obj: f"{obj.name} {'(전속)' if obj.is_exclusive else ''}"
    
    class Meta:
        model = Exhibition
        fields = [
            'title', 'title_en', 'slug', 'exhibition_type',
            'description', 'poster_image', 
            'start_date', 'end_date', 'opening_date',
            'venue', 'venue_address',
            'artists', 'is_current', 'is_featured', 'is_published',
            'meta_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '전시명'}),
            'title_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '영문 전시명'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL 슬러그'}),
            'exhibition_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'opening_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'venue': forms.TextInput(attrs={'class': 'form-control', 'value': '하나아트갤러리'}),
            'venue_address': forms.TextInput(attrs={'class': 'form-control'}),
            'artists': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 8}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = [
            'title', 'title_en', 'artist', 'artwork_type',
            'year', 'medium', 'size', 'edition',
            'description', 'main_image',
            'price', 'is_sold', 'is_for_sale',
            'exhibitions', 'is_featured', 'is_published', 'display_order'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'title_en': forms.TextInput(attrs={'class': 'form-control'}),
            'artist': forms.Select(attrs={'class': 'form-select'}),
            'artwork_type': forms.Select(attrs={'class': 'form-select'}),
            'year': forms.NumberInput(attrs={'class': 'form-control year-picker', 'placeholder': 'YYYY', 'min': '1900', 'max': '2099'}),
            'medium': forms.TextInput(attrs={'class': 'form-control'}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'edition': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'exhibitions': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_sold': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_for_sale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }