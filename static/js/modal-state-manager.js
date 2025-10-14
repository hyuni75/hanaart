/* ========================================
   하나아트갤러리 모달 상태 관리 및 토스트 메시지
   ======================================== */

(function() {
    'use strict';

    // 모달 상태 관리 객체
    window.ModalStateManager = {
        loadingModalVisible: false,
        activeModals: [],
        toastQueue: []
    };

    // 토스트 컨테이너 HTML (화면 중앙)
    const toastContainerHTML = `
        <div class="toast-container position-fixed top-50 start-50 translate-middle p-3" style="z-index: 9999;">
            <div id="commonToast" class="toast align-items-center border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body"></div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="닫기"></button>
                </div>
            </div>
        </div>
    `;

    // 로딩 모달 HTML
    const loadingModalHTML = `
        <div class="modal fade" id="loadingModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered modal-sm">
                <div class="modal-content bg-transparent border-0 shadow-none">
                    <div class="modal-body text-center text-white">
                        <div class="spinner-border" role="status" style="width: 3rem; height: 3rem;">
                            <span class="visually-hidden">로딩중...</span>
                        </div>
                        <p class="mt-3 mb-0" id="loadingMessage">처리 중입니다...</p>
                    </div>
                </div>
            </div>
        </div>
    `;

    // DOM 로드 완료 후 토스트 및 로딩 모달 삽입
    $(document).ready(function() {
        $('body').append(toastContainerHTML);
        $('body').append(loadingModalHTML);
    });

    /**
     * 토스트 메시지 표시 (화면 중앙)
     * @param {string} message - 표시할 메시지
     * @param {string} type - 메시지 타입 ('success', 'error', 'warning', 'info')
     * @param {number} duration - 표시 시간 (밀리초, 기본값: 3000)
     */
    window.showToast = function(message, type = 'info', duration = 3000) {
        const $toast = $('#commonToast');
        const $toastBody = $toast.find('.toast-body');

        // 타입별 스타일 클래스
        const typeClasses = {
            'success': 'text-bg-success',
            'error': 'text-bg-danger',
            'warning': 'text-bg-warning',
            'info': 'text-bg-info'
        };

        // 기존 클래스 제거 후 새 클래스 추가
        $toast.removeClass('text-bg-success text-bg-danger text-bg-warning text-bg-info');
        $toast.addClass(typeClasses[type] || typeClasses['info']);

        // 메시지 설정
        $toastBody.html(message.replace(/\n/g, '<br>'));

        // 토스트 표시
        const toast = new bootstrap.Toast($toast[0], {
            autohide: true,
            delay: duration
        });
        toast.show();
    };

    /**
     * 로딩 모달 표시
     * @param {string} message - 로딩 메시지 (기본값: '처리 중입니다...')
     */
    window.showLoading = function(message = '처리 중입니다...') {
        const $loadingModal = $('#loadingModal');
        $('#loadingMessage').text(message);

        window.ModalStateManager.loadingModalVisible = true;

        // 기존 인스턴스 확인 후 재사용
        let modal = bootstrap.Modal.getInstance($loadingModal[0]);
        if (!modal) {
            modal = new bootstrap.Modal($loadingModal[0], {
                backdrop: 'static',
                keyboard: false
            });
        }
        modal.show();
    };

    /**
     * 로딩 모달 숨김
     */
    window.hideLoading = function() {
        const $loadingModal = $('#loadingModal');

        // 로딩 모달이 존재하지 않으면 종료
        if ($loadingModal.length === 0) {
            window.ModalStateManager.loadingModalVisible = false;
            return;
        }

        // 상태 플래그 즉시 변경
        window.ModalStateManager.loadingModalVisible = false;

        // 로딩 모달 내부의 모든 요소에서 focus 제거 (aria-hidden 오류 방지)
        $loadingModal.find(':focus').blur();

        let modal = bootstrap.Modal.getInstance($loadingModal[0]);

        if (modal) {
            // 인스턴스가 있으면 hide() 호출
            modal.hide();
        }

        // Bootstrap 인스턴스 여부와 관계없이 강제로 숨김 처리 (확실하게)
        setTimeout(function() {
            $loadingModal.removeClass('show');
            $loadingModal.attr('aria-hidden', 'true');
            $loadingModal.css('display', 'none');

            // 로딩 모달의 backdrop은 항상 제거 (로딩 모달 전용 backdrop)
            // 다른 모달(생성/수정/삭제)은 자체 backdrop을 사용하므로 충돌하지 않음
            const $backdrops = $('.modal-backdrop');
            if ($backdrops.length > 0) {
                // 마지막 backdrop만 제거 (로딩 모달의 backdrop)
                $backdrops.last().remove();
            }

            // body 클래스 정리 (다른 모달이 없을 때만)
            if ($('.modal.show').length === 0) {
                $('body').removeClass('modal-open');
                $('body').css('overflow', '');
                $('body').css('padding-right', '');
            }
        }, 100);

        // 큐에 저장된 토스트 메시지 표시
        if (window.ModalStateManager.toastQueue.length > 0) {
            setTimeout(function() {
                window.ModalStateManager.toastQueue.forEach(function(toast) {
                    showToast(toast.message, toast.type, toast.duration);
                });
                window.ModalStateManager.toastQueue = [];
            }, 400); // 로딩 모달이 완전히 닫힌 후 표시
        }
    };

    /**
     * 모달 등록 (뒤로가기 처리용)
     * @param {string} modalId - 모달 ID
     */
    window.registerModal = function(modalId) {
        if (!window.ModalStateManager.activeModals.includes(modalId)) {
            window.ModalStateManager.activeModals.push(modalId);
        }
    };

    /**
     * 모달 해제 (뒤로가기 처리용)
     * @param {string} modalId - 모달 ID
     */
    window.unregisterModal = function(modalId) {
        const index = window.ModalStateManager.activeModals.indexOf(modalId);
        if (index > -1) {
            window.ModalStateManager.activeModals.splice(index, 1);
        }
    };

    /**
     * 모든 모달 닫기
     */
    window.closeAllModals = function() {
        // 모든 활성 모달 닫기
        window.ModalStateManager.activeModals.forEach(function(modalId) {
            const $modal = $(`#${modalId}`);

            // focus 제거 (aria-hidden 오류 방지)
            $modal.find(':focus').blur();

            const modal = bootstrap.Modal.getInstance($modal[0]);
            if (modal) {
                modal.hide();
            } else {
                // 인스턴스가 없으면 강제로 숨김
                $modal.removeClass('show');
                $modal.attr('aria-hidden', 'true');
                $modal.css('display', 'none');
            }
        });
        window.ModalStateManager.activeModals = [];

        // 로딩 모달도 닫기
        hideLoading();

        // 모든 backdrop 제거
        $('.modal-backdrop').remove();
        $('body').removeClass('modal-open');
        $('body').css('overflow', '');
        $('body').css('padding-right', '');
    };

    // 브라우저 뒤로가기 처리
    window.addEventListener('popstate', function() {
        closeAllModals();
    });

    // 모달이 열릴 때 등록
    $(document).on('show.bs.modal', '.modal', function() {
        const modalId = $(this).attr('id');
        if (modalId && modalId !== 'loadingModal') {
            registerModal(modalId);
        }
    });

    // 모달이 닫힐 때 해제
    $(document).on('hidden.bs.modal', '.modal', function() {
        const modalId = $(this).attr('id');
        if (modalId && modalId !== 'loadingModal') {
            unregisterModal(modalId);
        }
    });

})();
