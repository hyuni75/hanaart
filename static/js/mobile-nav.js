/* ========================================
   하나아트갤러리 모바일 네비게이션 시스템
   - 햄버거 슬라이드 메뉴 (좌측)
   - 터치 제스처 (스와이프)
   - 이미지 지연 로딩
   ======================================== */

(function($) {
    'use strict';

    /* ========================================
       MobileNavigation 클래스
       ======================================== */
    class MobileNavigation {
        constructor() {
            this.isOpen = false;
            this.isInitialized = false;
            this.eventsAttached = false;  // 이벤트 중복 등록 방지
            this.swipeEventsAttached = false;  // 스와이프 이벤트 중복 방지
            this.isTracking = false;  // 터치 추적 상태
            this.touchStartX = 0;
            this.touchStartY = 0;
            this.touchEndX = 0;
            this.touchEndY = 0;
            this.swipeThreshold = 80;
            this.screenEdgeThreshold = 30;

            this.init();
        }

        init() {
            // 992px 이하에서만 초기화
            if ($(window).width() < 992) {
                this.createMobileMenu();
                this.attachEventListeners();
                this.setupSwipeGestures();
                this.isInitialized = true;
                debugLog('MobileNavigation 초기화 완료');
            }

            // 화면 크기 변경 감지
            this.setupResizeHandler();
        }

        // 모바일 메뉴 HTML 동적 생성
        createMobileMenu() {
            // 이미 생성되어 있으면 스킵
            if ($('#mobileNavMenu').length > 0) {
                return;
            }

            // 기존 navbar에서 정보 추출
            const logoSrc = $('.navbar-brand img').attr('src');
            const navItems = [];

            // 기존 nav-link 복사
            $('.navbar-nav .nav-item').each(function() {
                const $link = $(this).find('a.nav-link');
                const href = $link.attr('href');
                const text = $link.text().trim();
                const isActive = $link.hasClass('active') || window.location.pathname === href;
                const isDanger = $link.hasClass('text-danger');

                navItems.push({
                    href: href,
                    text: text,
                    isActive: isActive,
                    isDanger: isDanger
                });
            });

            // 햄버거 버튼 생성
            const hamburgerHTML = `
                <button class="mobile-menu-toggle" id="mobileMenuToggle"
                        aria-label="메뉴 열기" aria-expanded="false" aria-controls="mobileNavMenu">
                    <div class="hamburger">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </button>
            `;

            // 오버레이와 메뉴 생성
            let menuItemsHTML = '';
            navItems.forEach(function(item) {
                let classes = 'mobile-nav-item';
                if (item.isActive) classes += ' active';
                if (item.isDanger) classes += ' admin-link';

                menuItemsHTML += `<a href="${item.href}" class="${classes}">${item.text}</a>`;
            });

            const mobileMenuHTML = `
                <!-- 오버레이 -->
                <div class="mobile-nav-overlay" id="mobileNavOverlay" aria-hidden="true"></div>

                <!-- 슬라이드 메뉴 -->
                <nav class="mobile-nav-menu" id="mobileNavMenu"
                     aria-label="모바일 네비게이션" role="navigation">
                    <div class="mobile-nav-header">
                        <div class="mobile-nav-logo">
                            <a href="/">
                                <img src="${logoSrc}" alt="하나아트갤러리">
                            </a>
                        </div>
                        <button class="mobile-nav-close" id="mobileNavClose"
                                aria-label="메뉴 닫기">&times;</button>
                    </div>
                    <div class="mobile-nav-items" id="mobileNavItems">
                        ${menuItemsHTML}
                    </div>
                </nav>
            `;

            // 기존 navbar-toggler 교체
            const $existingToggler = $('.navbar-toggler');
            if ($existingToggler.length > 0) {
                $existingToggler.replaceWith(hamburgerHTML);
            } else {
                // toggler가 없으면 navbar-brand 뒤에 추가
                $('.navbar-brand').after(hamburgerHTML);
            }

            // body에 오버레이와 메뉴 추가
            $('body').append(mobileMenuHTML);
        }

        // 이벤트 리스너 설정
        attachEventListeners() {
            // 이벤트 중복 등록 방지
            if (this.eventsAttached) return;
            this.eventsAttached = true;

            const self = this;

            // 햄버거 버튼 클릭
            $(document).on('click', '#mobileMenuToggle', function(e) {
                e.preventDefault();
                self.toggle();
            });

            // 닫기 버튼 클릭
            $(document).on('click', '#mobileNavClose', function(e) {
                e.preventDefault();
                self.close();
            });

            // 오버레이 클릭
            $(document).on('click', '#mobileNavOverlay', function() {
                self.close();
            });

            // 메뉴 아이템 클릭 시 메뉴 닫기
            $(document).on('click', '.mobile-nav-item', function() {
                // 약간의 지연 후 닫기 (클릭 피드백)
                setTimeout(function() {
                    self.close();
                }, 150);
            });

            // ESC 키로 메뉴 닫기
            $(document).on('keydown', function(e) {
                if (e.key === 'Escape' && self.isOpen) {
                    self.close();
                    $('#mobileMenuToggle').focus();
                }
            });

            // Tab 키 트랩 (접근성)
            $(document).on('keydown', '#mobileNavMenu', function(e) {
                if (e.key === 'Tab' && self.isOpen) {
                    self.handleTabTrap(e);
                }
            });
        }

        // Tab 키 트랩 (메뉴 내에서만 포커스 순환)
        handleTabTrap(e) {
            const $menu = $('#mobileNavMenu');
            // 모든 포커스 가능 요소 선택 (WCAG 2.1 준수)
            const focusableSelector = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
            const $focusable = $menu.find(focusableSelector).filter(':visible');
            const $first = $focusable.first();
            const $last = $focusable.last();

            if (e.shiftKey) {
                // Shift + Tab
                if (document.activeElement === $first[0]) {
                    e.preventDefault();
                    $last.focus();
                }
            } else {
                // Tab
                if (document.activeElement === $last[0]) {
                    e.preventDefault();
                    $first.focus();
                }
            }
        }

        // 화면 크기 변경 핸들러
        setupResizeHandler() {
            const self = this;
            let resizeTimer;

            $(window).on('resize', function() {
                clearTimeout(resizeTimer);
                resizeTimer = setTimeout(function() {
                    if ($(window).width() >= 992) {
                        // 데스크톱: 메뉴 닫기
                        if (self.isOpen) {
                            self.close();
                        }
                    } else if (!self.isInitialized) {
                        // 모바일로 전환: 초기화
                        self.createMobileMenu();
                        self.attachEventListeners();
                        self.setupSwipeGestures();
                        self.isInitialized = true;
                    }
                }, 150);
            });
        }

        // 메뉴 토글
        toggle() {
            if (this.isOpen) {
                this.close();
            } else {
                this.open();
            }
        }

        // 메뉴 열기
        open() {
            this.isOpen = true;

            const $toggle = $('#mobileMenuToggle');
            const $overlay = $('#mobileNavOverlay');
            const $menu = $('#mobileNavMenu');

            $toggle.addClass('active').attr('aria-expanded', 'true');
            $overlay.addClass('active').attr('aria-hidden', 'false');
            $menu.addClass('active');
            $('body').addClass('mobile-menu-open');

            // 첫 번째 메뉴 아이템에 포커스 (접근성)
            setTimeout(function() {
                $menu.find('.mobile-nav-item').first().focus();
            }, 300);

            debugLog('모바일 메뉴 열림');
        }

        // 메뉴 닫기
        close() {
            this.isOpen = false;

            const $toggle = $('#mobileMenuToggle');
            const $overlay = $('#mobileNavOverlay');
            const $menu = $('#mobileNavMenu');

            $toggle.removeClass('active').attr('aria-expanded', 'false');
            $overlay.removeClass('active').attr('aria-hidden', 'true');
            $menu.removeClass('active');
            $('body').removeClass('mobile-menu-open');

            debugLog('모바일 메뉴 닫힘');
        }

        // 터치 제스처 설정
        setupSwipeGestures() {
            // 스와이프 이벤트 중복 등록 방지
            if (this.swipeEventsAttached) return;
            this.swipeEventsAttached = true;

            const self = this;

            // 터치 시작 - 화면 가장자리 또는 메뉴가 열려있을 때만 추적
            $(document).on('touchstart.mobileNav', function(e) {
                const touchX = e.touches[0].clientX;

                // 메뉴가 열려있거나, 화면 왼쪽 가장자리에서 시작한 경우만 추적
                if (self.isOpen || touchX < self.screenEdgeThreshold) {
                    self.touchStartX = touchX;
                    self.touchStartY = e.touches[0].clientY;
                    self.isTracking = true;
                } else {
                    self.isTracking = false;
                }
            });

            // 터치 종료 - 추적 중인 경우만 처리
            $(document).on('touchend.mobileNav', function(e) {
                if (!self.isTracking) return;

                self.touchEndX = e.changedTouches[0].clientX;
                self.touchEndY = e.changedTouches[0].clientY;
                self.handleSwipe();
                self.isTracking = false;
            });
        }

        // 스와이프 처리
        handleSwipe() {
            const deltaX = this.touchEndX - this.touchStartX;
            const deltaY = this.touchEndY - this.touchStartY;

            // 수직 스와이프가 더 크면 무시 (스크롤 우선)
            if (Math.abs(deltaY) > Math.abs(deltaX)) {
                return;
            }

            // 최소 스와이프 거리 체크
            if (Math.abs(deltaX) < this.swipeThreshold) {
                return;
            }

            // 좌에서 우로 스와이프: 메뉴 열기
            if (deltaX > 0 && !this.isOpen) {
                // 화면 왼쪽 가장자리에서 시작한 경우만
                if (this.touchStartX < this.screenEdgeThreshold) {
                    this.open();
                }
            }

            // 우에서 좌로 스와이프: 메뉴 닫기
            if (deltaX < 0 && this.isOpen) {
                this.close();
            }
        }
    }

    /* ========================================
       LazyLoading 클래스 (이미지 지연 로딩)
       ======================================== */
    class LazyLoading {
        constructor() {
            this.observer = null;
            this.init();
        }

        init() {
            if ('IntersectionObserver' in window) {
                this.setupObserver();
                this.observeImages();
            } else {
                // Intersection Observer 미지원 (IE11 등)
                this.loadAllImages();
            }

            debugLog('LazyLoading 초기화 완료');
        }

        setupObserver() {
            const self = this;

            this.observer = new IntersectionObserver(function(entries, observer) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        self.loadImage(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                rootMargin: '50px 0px', // 뷰포트 50px 전에 로드 시작
                threshold: 0.01
            });
        }

        observeImages() {
            const self = this;

            $('img[data-lazy]').each(function() {
                self.observer.observe(this);
                $(this).addClass('lazy-loading');
            });
        }

        loadImage(img) {
            const $img = $(img);
            const src = $img.attr('data-lazy');

            if (src) {
                // 이미지 프리로드
                const tempImg = new Image();
                tempImg.onload = function() {
                    $img.attr('src', src);
                    $img.removeClass('lazy-loading').addClass('loaded');
                    $img.removeAttr('data-lazy');
                };
                tempImg.onerror = function() {
                    debugLog('이미지 로드 실패:', src);
                    $img.removeClass('lazy-loading').addClass('load-error');
                    // 에러 플레이스홀더 이미지 또는 스타일 적용
                    $img.attr('alt', $img.attr('alt') || '이미지를 불러올 수 없습니다');
                    $img.removeAttr('data-lazy');
                };
                tempImg.src = src;
            }
        }

        loadAllImages() {
            // Fallback: 즉시 로드
            $('img[data-lazy]').each(function() {
                const $img = $(this);
                const src = $img.attr('data-lazy');
                $img.attr('src', src).addClass('loaded').removeAttr('data-lazy');
            });
        }
    }

    /* ========================================
       TouchOptimization 클래스
       ======================================== */
    class TouchOptimization {
        constructor() {
            this.init();
        }

        init() {
            if ('ontouchstart' in window) {
                this.improveCardInteraction();
                this.enablePassiveListeners();
            }
        }

        // 카드 터치 피드백
        improveCardInteraction() {
            $(document).on('touchstart', '.card, .gallery-item', function() {
                $(this).addClass('touch-active');
            });

            $(document).on('touchend touchcancel', '.card, .gallery-item', function() {
                $(this).removeClass('touch-active');
            });
        }

        // Passive Event Listeners (스크롤 성능)
        enablePassiveListeners() {
            // 기본 touchstart/touchmove를 passive로 등록
            try {
                const passiveSupported = this.checkPassiveSupport();
                if (passiveSupported) {
                    document.addEventListener('touchstart', function() {}, { passive: true });
                    document.addEventListener('touchmove', function() {}, { passive: true });
                }
            } catch (e) {
                debugLog('Passive listeners 설정 실패:', e);
            }
        }

        checkPassiveSupport() {
            let passiveSupported = false;
            try {
                const options = {
                    get passive() {
                        passiveSupported = true;
                        return false;
                    }
                };
                window.addEventListener('test', null, options);
                window.removeEventListener('test', null, options);
            } catch (err) {
                passiveSupported = false;
            }
            return passiveSupported;
        }
    }

    /* ========================================
       ViewportDetector (Breakpoint 감지)
       ======================================== */
    class ViewportDetector {
        constructor() {
            this.currentBreakpoint = null;
            this.breakpoints = {
                xs: 0,
                sm: 576,
                md: 768,
                lg: 992,
                xl: 1200,
                xxl: 1400
            };

            this.init();
        }

        init() {
            this.detectBreakpoint();

            const self = this;
            $(window).on('resize', function() {
                self.detectBreakpoint();
            });
        }

        detectBreakpoint() {
            const width = $(window).width();
            let newBreakpoint = 'xs';

            for (const [key, value] of Object.entries(this.breakpoints)) {
                if (width >= value) {
                    newBreakpoint = key;
                }
            }

            if (this.currentBreakpoint !== newBreakpoint) {
                this.currentBreakpoint = newBreakpoint;
                $(document).trigger('breakpointChange', [newBreakpoint, width]);
                debugLog('Breakpoint 변경:', newBreakpoint, width + 'px');
            }
        }

        getCurrentBreakpoint() {
            return this.currentBreakpoint;
        }

        isMobile() {
            return ['xs', 'sm', 'md'].includes(this.currentBreakpoint);
        }

        isDesktop() {
            return ['lg', 'xl', 'xxl'].includes(this.currentBreakpoint);
        }
    }

    /* ========================================
       초기화
       ======================================== */
    $(document).ready(function() {
        // Viewport 감지
        window.viewportDetector = new ViewportDetector();

        // 모바일 네비게이션
        window.mobileNav = new MobileNavigation();

        // 이미지 지연 로딩
        window.lazyLoading = new LazyLoading();

        // 터치 최적화
        window.touchOptimization = new TouchOptimization();

        debugLog('모바일 반응형 시스템 초기화 완료');
    });

})(jQuery);
