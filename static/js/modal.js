/**
 * 공통 모달 시스템
 * CLAUDE.md 규칙에 따라 브라우저 alert 대신 사용
 */

class HanaModal {
    constructor() {
        this.modal = null;
        this.init();
    }

    init() {
        // 모달 HTML이 없으면 동적으로 생성
        if (!document.getElementById('commonModal')) {
            this.createModalHTML();
        }
        this.modal = new bootstrap.Modal(document.getElementById('commonModal'));
    }

    createModalHTML() {
        const modalHTML = `
            <div class="modal fade" id="commonModal" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header border-0">
                            <h5 class="modal-title" id="commonModalTitle">알림</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body text-center py-4" id="commonModalBody">
                            메시지
                        </div>
                        <div class="modal-footer border-0" id="commonModalFooter">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">닫기</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    /**
     * 정보 모달 표시
     */
    info(message, title = '알림') {
        this.show(message, title, 'info');
    }

    /**
     * 성공 모달 표시
     */
    success(message, title = '성공') {
        this.show(message, title, 'success');
    }

    /**
     * 경고 모달 표시
     */
    warning(message, title = '경고') {
        this.show(message, title, 'warning');
    }

    /**
     * 오류 모달 표시
     */
    error(message, title = '오류') {
        this.show(message, title, 'error');
    }

    /**
     * 확인 모달 표시 (확인/취소 버튼)
     */
    confirm(message, title = '확인', onConfirm = null, onCancel = null) {
        const modalEl = document.getElementById('commonModal');
        const titleEl = document.getElementById('commonModalTitle');
        const bodyEl = document.getElementById('commonModalBody');
        const footerEl = document.getElementById('commonModalFooter');

        // 모달 스타일 초기화
        modalEl.className = 'modal fade modal-confirm';
        
        // 제목과 내용 설정
        titleEl.innerHTML = `<i class="fas fa-question-circle text-primary me-2"></i>${title}`;
        bodyEl.innerHTML = message;

        // 확인/취소 버튼 설정
        footerEl.innerHTML = `
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">취소</button>
            <button type="button" class="btn btn-primary" id="confirmBtn">확인</button>
        `;

        // 확인 버튼 클릭 이벤트
        const confirmBtn = document.getElementById('confirmBtn');
        confirmBtn.onclick = () => {
            this.modal.hide();
            if (onConfirm) onConfirm();
        };

        // 취소 시 콜백
        modalEl.addEventListener('hidden.bs.modal', function handler() {
            modalEl.removeEventListener('hidden.bs.modal', handler);
            if (onCancel && !confirmBtn.clicked) onCancel();
        }, { once: true });

        this.modal.show();
        return this;
    }

    /**
     * 삭제 확인 모달
     */
    confirmDelete(itemName, onConfirm) {
        const message = `정말로 <strong>${itemName}</strong>을(를) 삭제하시겠습니까?<br>
                        <span class="text-danger">이 작업은 되돌릴 수 없습니다.</span>`;
        const title = '삭제 확인';
        
        const modalEl = document.getElementById('commonModal');
        const titleEl = document.getElementById('commonModalTitle');
        const bodyEl = document.getElementById('commonModalBody');
        const footerEl = document.getElementById('commonModalFooter');

        modalEl.className = 'modal fade modal-delete';
        titleEl.innerHTML = `<i class="fas fa-trash text-danger me-2"></i>${title}`;
        bodyEl.innerHTML = message;
        
        footerEl.innerHTML = `
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">취소</button>
            <button type="button" class="btn btn-danger" id="deleteConfirmBtn">
                <i class="fas fa-trash me-1"></i>삭제
            </button>
        `;

        document.getElementById('deleteConfirmBtn').onclick = () => {
            this.modal.hide();
            if (onConfirm) onConfirm();
        };

        this.modal.show();
        return this;
    }

    /**
     * 기본 모달 표시
     */
    show(message, title = '알림', type = 'info') {
        const modalEl = document.getElementById('commonModal');
        const titleEl = document.getElementById('commonModalTitle');
        const bodyEl = document.getElementById('commonModalBody');
        const footerEl = document.getElementById('commonModalFooter');

        // 타입별 아이콘과 스타일 설정
        const icons = {
            info: '<i class="fas fa-info-circle text-info me-2"></i>',
            success: '<i class="fas fa-check-circle text-success me-2"></i>',
            warning: '<i class="fas fa-exclamation-triangle text-warning me-2"></i>',
            error: '<i class="fas fa-times-circle text-danger me-2"></i>'
        };

        modalEl.className = `modal fade modal-${type}`;
        titleEl.innerHTML = (icons[type] || '') + title;
        bodyEl.innerHTML = message;
        
        // 기본 닫기 버튼
        footerEl.innerHTML = `
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal">확인</button>
        `;

        this.modal.show();
        return this;
    }

    /**
     * 모달 숨기기
     */
    hide() {
        if (this.modal) {
            this.modal.hide();
        }
    }
}

// 전역 모달 인스턴스
window.hanaModal = new HanaModal();