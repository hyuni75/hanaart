/* ========================================
   하나아트갤러리 공통 모달 갤러리
   작품 감상용 큰 이미지 모달
   ======================================== */

(function() {
    'use strict';

    // 모달 HTML 생성 (페이지 로드 시 자동 삽입)
    const modalHTML = `
    <div class="modal fade modal-gallery" id="galleryModal" tabindex="-1" aria-labelledby="galleryModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-body p-0">
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="닫기"></button>

                    <div id="galleryCarousel" class="carousel slide" data-bs-ride="false">
                        <div class="carousel-inner" id="galleryCarouselInner">
                            <!-- 이미지 슬라이드가 동적으로 추가됩니다 -->
                        </div>

                        <!-- 좌우 화살표 -->
                        <button class="carousel-control-prev" type="button" data-bs-target="#galleryCarousel" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">이전</span>
                        </button>
                        <button class="carousel-control-next" type="button" data-bs-target="#galleryCarousel" data-bs-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">다음</span>
                        </button>

                        <!-- 페이지 인디케이터 -->
                        <div class="carousel-indicators" id="galleryCarouselIndicators">
                            <!-- 인디케이터가 동적으로 추가됩니다 -->
                        </div>
                    </div>

                    <!-- 작품 정보 -->
                    <div class="modal-artwork-info text-white p-4">
                        <h5 id="artworkTitle" class="mb-2"></h5>
                        <p id="artworkDetails" class="mb-0 text-muted"></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `;

    // DOM 로드 완료 후 모달 삽입
    $(document).ready(function() {
        $('body').append(modalHTML);
    });

    /**
     * 갤러리 모달 열기
     * @param {Array} artworks - 작품 배열 [{image, title, artist, year, size, material}, ...]
     * @param {Number} initialIndex - 시작 인덱스 (기본값: 0)
     */
    window.openGalleryModal = function(artworks, initialIndex = 0) {
        if (!artworks || artworks.length === 0) {
            console.error('작품 데이터가 없습니다.');
            return;
        }

        const $modal = $('#galleryModal');
        const $carouselInner = $('#galleryCarouselInner');
        const $indicators = $('#galleryCarouselIndicators');

        // 기존 내용 초기화
        $carouselInner.empty();
        $indicators.empty();

        // 슬라이드 및 인디케이터 생성
        artworks.forEach((artwork, index) => {
            const isActive = index === initialIndex ? 'active' : '';

            // 슬라이드 아이템
            const slideHTML = `
                <div class="carousel-item ${isActive}">
                    <img src="${artwork.image}" class="d-block w-100 modal-gallery-img" alt="${artwork.title}">
                </div>
            `;
            $carouselInner.append(slideHTML);

            // 인디케이터
            const indicatorHTML = `
                <button type="button"
                        data-bs-target="#galleryCarousel"
                        data-bs-slide-to="${index}"
                        class="${isActive}"
                        aria-current="${isActive ? 'true' : 'false'}"
                        aria-label="슬라이드 ${index + 1}">
                </button>
            `;
            $indicators.append(indicatorHTML);
        });

        // Carousel 이벤트: 슬라이드 변경 시 작품 정보 업데이트
        const carousel = new bootstrap.Carousel(document.getElementById('galleryCarousel'), {
            interval: false // 자동 슬라이드 비활성화
        });

        $('#galleryCarousel').off('slide.bs.carousel').on('slide.bs.carousel', function(e) {
            updateArtworkInfo(artworks[e.to]);
        });

        // 초기 작품 정보 표시
        updateArtworkInfo(artworks[initialIndex]);

        // 모달 열기
        const modal = new bootstrap.Modal($modal[0]);
        modal.show();
    };

    /**
     * 작품 정보 업데이트
     * @param {Object} artwork - 작품 객체
     */
    function updateArtworkInfo(artwork) {
        $('#artworkTitle').text(artwork.title || '제목 없음');

        let details = [];
        if (artwork.artist) details.push(artwork.artist);
        if (artwork.year) details.push(artwork.year + '년');
        if (artwork.size) details.push(artwork.size);
        if (artwork.material) details.push(artwork.material);

        $('#artworkDetails').text(details.join(' | '));
    }

    /**
     * 갤러리 아이템 클릭 이벤트 자동 바인딩
     * data-gallery 속성을 가진 요소에 자동으로 클릭 이벤트 연결
     */
    $(document).on('click', '[data-gallery]', function(e) {
        e.preventDefault();

        const galleryName = $(this).data('gallery');
        const index = $(this).data('index') || 0;

        // 같은 갤러리 그룹의 모든 아이템 수집
        const $galleryItems = $(`[data-gallery="${galleryName}"]`);
        const artworks = [];

        $galleryItems.each(function() {
            artworks.push({
                image: $(this).data('image'),
                title: $(this).data('title') || '',
                artist: $(this).data('artist') || '',
                year: $(this).data('year') || '',
                size: $(this).data('size') || '',
                material: $(this).data('material') || ''
            });
        });

        openGalleryModal(artworks, index);
    });

})();
