/**
 * 공통 토스트 시스템
 * CLAUDE.md 규칙에 따라 일관된 사용자 경험 제공
 */

class HanaToast {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {
        // 토스트 컨테이너가 없으면 생성
        if (!document.getElementById('toastContainer')) {
            this.createToastContainer();
        }
        this.container = document.getElementById('toastContainer');
    }

    createToastContainer() {
        const containerHTML = `
            <div id="toastContainer" class="toast-container position-fixed top-50 start-50 translate-middle" style="z-index: 9999;">
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', containerHTML);
    }

    /**
     * 토스트 생성 및 표시
     */
    show(message, type = 'info', duration = 3000) {
        const toastId = 'toast_' + Date.now();
        
        // 타입별 설정
        const configs = {
            info: {
                icon: 'fa-info-circle',
                bgClass: 'bg-info',
                textClass: 'text-white'
            },
            success: {
                icon: 'fa-check-circle',
                bgClass: 'bg-success',
                textClass: 'text-white'
            },
            warning: {
                icon: 'fa-exclamation-triangle',
                bgClass: 'bg-warning',
                textClass: 'text-dark'
            },
            error: {
                icon: 'fa-times-circle',
                bgClass: 'bg-danger',
                textClass: 'text-white'
            }
        };

        const config = configs[type] || configs.info;

        const toastHTML = `
            <div id="${toastId}" class="toast align-items-center ${config.bgClass} ${config.textClass} border-0 mb-3 shadow-lg" 
                 role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body d-flex align-items-center">
                        <i class="fas ${config.icon} me-2" style="font-size: 1.2rem;"></i>
                        <span style="font-size: 1rem; font-weight: 500;">${message}</span>
                    </div>
                    <button type="button" class="btn-close btn-close-${config.textClass === 'text-white' ? 'white' : 'dark'} me-2 m-auto" 
                            data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;

        // 토스트 추가
        this.container.insertAdjacentHTML('beforeend', toastHTML);
        
        // Bootstrap 토스트 초기화 및 표시
        const toastEl = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastEl, {
            delay: duration,
            animation: true
        });
        
        // 토스트 제거 이벤트
        toastEl.addEventListener('hidden.bs.toast', () => {
            toastEl.remove();
        });

        toast.show();

        // 애니메이션 효과
        setTimeout(() => {
            toastEl.style.animation = 'slideInDown 0.3s ease-out';
        }, 10);

        return this;
    }

    /**
     * 정보 토스트
     */
    info(message, duration = 3000) {
        return this.show(message, 'info', duration);
    }

    /**
     * 성공 토스트
     */
    success(message, duration = 3000) {
        return this.show(message, 'success', duration);
    }

    /**
     * 경고 토스트
     */
    warning(message, duration = 4000) {
        return this.show(message, 'warning', duration);
    }

    /**
     * 오류 토스트
     */
    error(message, duration = 5000) {
        return this.show(message, 'error', duration);
    }

    /**
     * 로딩 토스트 (자동으로 사라지지 않음)
     */
    loading(message = '처리 중...') {
        const toastId = 'toast_loading';
        
        // 기존 로딩 토스트 제거
        const existingToast = document.getElementById(toastId);
        if (existingToast) {
            existingToast.remove();
        }

        const toastHTML = `
            <div id="${toastId}" class="toast align-items-center bg-primary text-white border-0 mb-3 shadow-lg" 
                 role="status" aria-live="polite" aria-atomic="true" data-bs-autohide="false">
                <div class="d-flex">
                    <div class="toast-body d-flex align-items-center">
                        <div class="spinner-border spinner-border-sm me-2" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <span style="font-size: 1rem; font-weight: 500;">${message}</span>
                    </div>
                </div>
            </div>
        `;

        this.container.insertAdjacentHTML('beforeend', toastHTML);
        
        const toastEl = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastEl, {
            autohide: false
        });
        
        toast.show();

        // 로딩 토스트 숨기기 메서드
        return {
            hide: () => {
                const loadingToast = document.getElementById(toastId);
                if (loadingToast) {
                    const bsToast = bootstrap.Toast.getInstance(loadingToast);
                    if (bsToast) {
                        bsToast.hide();
                        setTimeout(() => loadingToast.remove(), 300);
                    }
                }
            }
        };
    }

    /**
     * 모든 토스트 제거
     */
    clear() {
        if (this.container) {
            this.container.innerHTML = '';
        }
    }
}

// 전역 토스트 인스턴스
window.hanaToast = new HanaToast();

// CSS 애니메이션 추가
if (!document.getElementById('toastAnimationStyles')) {
    const style = document.createElement('style');
    style.id = 'toastAnimationStyles';
    style.textContent = `
        @keyframes slideInDown {
            from {
                transform: translate(-50%, -150%);
                opacity: 0;
            }
            to {
                transform: translate(-50%, -50%);
                opacity: 1;
            }
        }
        
        .toast {
            min-width: 350px;
            max-width: 500px;
            font-family: 'Noto Sans KR', sans-serif;
        }
        
        .toast-container {
            pointer-events: none;
        }
        
        .toast-container .toast {
            pointer-events: auto;
        }
    `;
    document.head.appendChild(style);
}