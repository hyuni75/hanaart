/* ========================================
   하나아트갤러리 공통 CRUD 모달 시스템
   모든 관리자 페이지에서 사용
   ======================================== */

(function() {
    'use strict';

    /**
     * 상세 정보 모달 표시
     * @param {string} title - 모달 제목
     * @param {string} content - 모달 내용 (HTML 허용)
     * @param {Object} options - 추가 옵션
     */
    window.showDetailModal = function(title, content, options = {}) {
        const modalId = options.modalId || 'detailModal';
        let $modal = $(`#${modalId}`);

        // 모달이 없으면 동적 생성
        if ($modal.length === 0) {
            const modalHTML = `
                <div class="modal fade" id="${modalId}" tabindex="-1">
                    <div class="modal-dialog ${options.size || 'modal-lg'}">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">${title}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="닫기"></button>
                            </div>
                            <div class="modal-body">
                                ${content}
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">닫기</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            $('body').append(modalHTML);
            $modal = $(`#${modalId}`);
        } else {
            // 기존 모달 내용 업데이트
            $modal.find('.modal-title').text(title);
            $modal.find('.modal-body').html(content);
        }

        // 모달 표시 (기존 인스턴스 재사용)
        let modal = bootstrap.Modal.getInstance($modal[0]);
        if (!modal) {
            modal = new bootstrap.Modal($modal[0]);
        }
        modal.show();

        // 닫기 시 제거 (옵션)
        if (options.removeOnClose) {
            $modal.on('hidden.bs.modal', function() {
                $modal.remove();
            });
        }
    };

    /**
     * 수정 모달 표시 (폼 포함)
     * @param {string} title - 모달 제목
     * @param {string} formContent - 폼 내용 (HTML)
     * @param {Function} onSave - 저장 버튼 클릭 시 콜백 함수
     * @param {Object} options - 추가 옵션
     */
    window.showEditModal = function(title, formContent, onSave, options = {}) {
        const modalId = options.modalId || 'editModal';
        let $modal = $(`#${modalId}`);

        // 모달이 없으면 동적 생성
        if ($modal.length === 0) {
            const modalHTML = `
                <div class="modal fade" id="${modalId}" tabindex="-1">
                    <div class="modal-dialog ${options.size || 'modal-lg'}">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">${title}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="닫기"></button>
                            </div>
                            <div class="modal-body">
                                ${formContent}
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">취소</button>
                                <button type="button" class="btn btn-primary" id="${modalId}SaveBtn">수정</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            $('body').append(modalHTML);
            $modal = $(`#${modalId}`);
        } else {
            // 기존 모달 내용 업데이트
            $modal.find('.modal-title').text(title);
            $modal.find('.modal-body').html(formContent);
            // 기존 버튼을 모두 제거하고 새로 생성
            $modal.find('.modal-footer').html(`
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">취소</button>
                <button type="button" class="btn btn-primary" id="${modalId}SaveBtn">수정</button>
            `);
        }

        // 저장 버튼 이벤트 바인딩
        $modal.find(`#${modalId}SaveBtn`).off('click').on('click', function() {
            if (typeof onSave === 'function') {
                onSave($modal);
            }
        });

        // 취소 버튼에 명시적인 닫기 이벤트 추가
        $modal.find('[data-bs-dismiss="modal"]').off('click').on('click', function() {
            closeModal($modal);
        });

        // 모달 표시 (기존 인스턴스 재사용)
        let modal = bootstrap.Modal.getInstance($modal[0]);
        if (!modal) {
            modal = new bootstrap.Modal($modal[0]);
        }
        modal.show();

        // 닫기 시 제거 (옵션)
        if (options.removeOnClose) {
            $modal.on('hidden.bs.modal', function() {
                $modal.remove();
            });
        }
    };

    /**
     * 생성 모달 표시 (폼 포함)
     * @param {string} title - 모달 제목
     * @param {string} formContent - 폼 내용 (HTML)
     * @param {Function} onCreate - 생성 버튼 클릭 시 콜백 함수
     * @param {Object} options - 추가 옵션
     */
    window.showCreateModal = function(title, formContent, onCreate, options = {}) {
        const modalId = options.modalId || 'createModal';
        let $modal = $(`#${modalId}`);

        // 모달이 없으면 동적 생성
        if ($modal.length === 0) {
            const modalHTML = `
                <div class="modal fade" id="${modalId}" tabindex="-1">
                    <div class="modal-dialog ${options.size || 'modal-lg'}">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">${title}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="닫기"></button>
                            </div>
                            <div class="modal-body">
                                ${formContent}
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">취소</button>
                                <button type="button" class="btn btn-primary" id="${modalId}CreateBtn">저장</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            $('body').append(modalHTML);
            $modal = $(`#${modalId}`);
        } else {
            // 기존 모달 내용 업데이트
            $modal.find('.modal-title').text(title);
            $modal.find('.modal-body').html(formContent);
            // 기존 버튼을 모두 제거하고 새로 생성
            $modal.find('.modal-footer').html(`
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">취소</button>
                <button type="button" class="btn btn-primary" id="${modalId}CreateBtn">저장</button>
            `);
        }

        // 생성 버튼 이벤트 바인딩
        $modal.find(`#${modalId}CreateBtn`).off('click').on('click', function() {
            if (typeof onCreate === 'function') {
                onCreate($modal);
            }
        });

        // 취소 버튼에 명시적인 닫기 이벤트 추가
        $modal.find('[data-bs-dismiss="modal"]').off('click').on('click', function() {
            closeModal($modal);
        });

        // 모달 표시 (기존 인스턴스 재사용)
        let modal = bootstrap.Modal.getInstance($modal[0]);
        if (!modal) {
            modal = new bootstrap.Modal($modal[0]);
        }
        modal.show();

        // 닫기 시 제거 (옵션)
        if (options.removeOnClose) {
            $modal.on('hidden.bs.modal', function() {
                $modal.remove();
            });
        }
    };

    /**
     * 삭제 확인 모달 표시
     * @param {string} message - 확인 메시지
     * @param {Function} onConfirm - 확인 버튼 클릭 시 콜백 함수
     * @param {Object} options - 추가 옵션
     */
    window.showDeleteModal = function(message, onConfirm, options = {}) {
        const modalId = options.modalId || 'deleteConfirmModal';
        const title = options.title || '삭제 확인';
        const confirmBtnText = options.confirmBtnText || '삭제';
        const dangerText = options.dangerText || '';

        let $modal = $(`#${modalId}`);

        // 모달이 없으면 동적 생성
        if ($modal.length === 0) {
            const modalHTML = `
                <div class="modal fade" id="${modalId}" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">${title}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="닫기"></button>
                            </div>
                            <div class="modal-body">
                                <p>${message}</p>
                                ${dangerText ? `<p class="text-danger"><strong>${dangerText}</strong></p>` : ''}
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">취소</button>
                                <button type="button" class="btn btn-danger" id="${modalId}ConfirmBtn">${confirmBtnText}</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            $('body').append(modalHTML);
            $modal = $(`#${modalId}`);
        } else {
            // 기존 모달 내용 업데이트
            $modal.find('.modal-title').text(title);
            $modal.find('.modal-body').html(`
                <p>${message}</p>
                ${dangerText ? `<p class="text-danger"><strong>${dangerText}</strong></p>` : ''}
            `);
        }

        // 확인 버튼 이벤트 바인딩
        $modal.find(`#${modalId}ConfirmBtn`).off('click').on('click', function() {
            if (typeof onConfirm === 'function') {
                onConfirm($modal);
            }
        });

        // 취소 버튼에 명시적인 닫기 이벤트 추가
        $modal.find('[data-bs-dismiss="modal"]').off('click').on('click', function() {
            closeModal($modal);
        });

        // 모달 표시 (기존 인스턴스 재사용)
        let modal = bootstrap.Modal.getInstance($modal[0]);
        if (!modal) {
            modal = new bootstrap.Modal($modal[0]);
        }
        modal.show();

        // 닫기 시 제거 (옵션)
        if (options.removeOnClose) {
            $modal.on('hidden.bs.modal', function() {
                $modal.remove();
            });
        }
    };

    /**
     * 커스텀 모달 표시 (다중 인터페이스 지원)
     * @param {string|Object} titleOrConfig - 모달 제목 또는 설정 객체
     * @param {string} content - 모달 내용 (HTML 허용) - titleOrConfig가 문자열일 때 사용
     * @param {Function} onConfirm - 확인 버튼 클릭 시 콜백 함수 - titleOrConfig가 문자열일 때 사용
     * @param {Function} onCancel - 취소 버튼 클릭 시 콜백 함수 - titleOrConfig가 문자열일 때 사용
     * @param {Object} options - 추가 옵션 - titleOrConfig가 문자열일 때 사용
     *
     * @example
     * // 방법 1: 객체 방식 (기존)
     * showCustomModal({
     *     title: '제목',
     *     content: '내용',
     *     size: 'modal-lg',
     *     buttons: [
     *         { text: '취소', class: 'btn-secondary', dismiss: true },
     *         { text: '확인', class: 'btn-primary', onClick: function($modal) { ... } }
     *     ]
     * })
     *
     * // 방법 2: 간편 방식 (신규)
     * showCustomModal('제목', '내용', function($modal) { 확인 }, function($modal) { 취소 }, { modalId: 'myModal', confirmText: '확인', cancelText: '취소' })
     */
    window.showCustomModal = function(titleOrConfig, content, onConfirm, onCancel, options) {
        let config;

        // 첫 번째 인자가 객체면 기존 방식, 문자열이면 간편 방식
        if (typeof titleOrConfig === 'object') {
            config = titleOrConfig;
        } else {
            // 간편 방식: 인자로 받은 값들을 config 객체로 변환
            options = options || {};
            const confirmText = options.confirmText || '확인';
            const cancelText = options.cancelText || '취소';
            const confirmClass = options.confirmClass || 'btn-primary';

            config = {
                modalId: options.modalId || 'customModal' + Date.now(),
                title: titleOrConfig,
                content: content,
                size: options.size || '',
                buttons: []
            };

            // 취소 버튼 추가 (onCancel이 있거나 명시적으로 취소 버튼이 필요한 경우)
            if (onCancel || !onConfirm) {
                config.buttons.push({
                    text: cancelText,
                    class: 'btn-secondary',
                    onClick: onCancel,
                    dismiss: !onCancel // 콜백이 없으면 자동 닫기
                });
            }

            // 확인 버튼 추가
            if (onConfirm) {
                config.buttons.push({
                    text: confirmText,
                    class: confirmClass,
                    onClick: onConfirm
                });
            }
        }

        const modalId = config.modalId || 'customModal' + Date.now();
        const title = config.title || '알림';
        const modalContent = config.content || '';
        const size = config.size || '';
        const buttons = config.buttons || [
            { text: '닫기', class: 'btn-secondary', dismiss: true }
        ];

        // 버튼 HTML 생성
        let buttonsHTML = '';
        buttons.forEach(function(btn, index) {
            const btnId = `${modalId}Btn${index}`;
            const dismissAttr = btn.dismiss ? 'data-bs-dismiss="modal"' : '';
            buttonsHTML += `
                <button type="button" class="btn ${btn.class}" id="${btnId}" ${dismissAttr}>
                    ${btn.text}
                </button>
            `;
        });

        // 모달 HTML 생성
        const modalHTML = `
            <div class="modal fade" id="${modalId}" tabindex="-1">
                <div class="modal-dialog ${size}">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="닫기"></button>
                        </div>
                        <div class="modal-body">
                            ${modalContent}
                        </div>
                        <div class="modal-footer">
                            ${buttonsHTML}
                        </div>
                    </div>
                </div>
            </div>
        `;

        $('body').append(modalHTML);
        const $modal = $(`#${modalId}`);

        // 버튼 이벤트 바인딩
        buttons.forEach(function(btn, index) {
            if (btn.onClick && typeof btn.onClick === 'function') {
                $modal.find(`#${modalId}Btn${index}`).on('click', function() {
                    btn.onClick($modal);
                });
            }
        });

        // 모달 표시 (기존 인스턴스 재사용)
        let modal = bootstrap.Modal.getInstance($modal[0]);
        if (!modal) {
            modal = new bootstrap.Modal($modal[0]);
        }
        modal.show();

        // 닫기 시 DOM에서 제거
        $modal.on('hidden.bs.modal', function() {
            $modal.remove();
        });
    };

    /**
     * 모달 닫기 (다중 인터페이스 지원)
     * @param {string|jQuery|HTMLElement} modalIdOrElement - 닫을 모달 ID 또는 jQuery 객체 또는 DOM 요소
     * @example
     * closeModal('myModalId')  // ID로 닫기
     * closeModal($modal)       // jQuery 객체로 닫기
     * closeModal(modalElement) // DOM 요소로 닫기
     */
    window.closeModal = function(modalIdOrElement) {
        let $modal;

        if (typeof modalIdOrElement === 'string') {
            // 문자열이면 ID로 판단
            $modal = $(`#${modalIdOrElement}`);
        } else if (modalIdOrElement instanceof jQuery) {
            // jQuery 객체면 그대로 사용
            $modal = modalIdOrElement;
        } else if (modalIdOrElement instanceof HTMLElement) {
            // DOM 요소면 jQuery로 감싸기
            $modal = $(modalIdOrElement);
        } else {
            console.error('closeModal: 유효하지 않은 인자', modalIdOrElement);
            return;
        }

        // 모달 요소가 존재하는지 확인
        if ($modal.length === 0) {
            console.warn('closeModal: 모달을 찾을 수 없습니다', modalIdOrElement);
            return;
        }

        // 모달 내부의 모든 요소에서 focus 제거 (aria-hidden 오류 방지)
        $modal.find(':focus').blur();

        // Bootstrap 모달 인스턴스 가져오기 (없으면 생성하지 않음)
        let modal = bootstrap.Modal.getInstance($modal[0]);

        if (modal) {
            // 인스턴스가 있으면 hide() 호출
            modal.hide();
        }

        // Bootstrap 인스턴스 여부와 관계없이 강제로 숨김 처리 (확실하게)
        setTimeout(function() {
            $modal.removeClass('show');
            $modal.attr('aria-hidden', 'true');
            $modal.css('display', 'none');

            // 해당 모달의 backdrop만 제거 (다른 모달은 건드리지 않음)
            const modalId = $modal.attr('id');
            const $backdrops = $('.modal-backdrop');

            // 다른 열린 모달이 없을 때만 backdrop과 body 클래스 제거
            if ($('.modal.show').length === 0) {
                $backdrops.remove();
                $('body').removeClass('modal-open');
                $('body').css('overflow', '');
                $('body').css('padding-right', '');
            }
        }, 200);
    };

    /**
     * 확인 다이얼로그 (alert 대체)
     * @param {string} message - 메시지
     * @param {string} title - 제목 (기본값: '알림')
     */
    window.showAlert = function(message, title = '알림') {
        showCustomModal({
            title: title,
            content: `<p>${message}</p>`,
            buttons: [
                { text: '확인', class: 'btn-primary', dismiss: true }
            ],
            removeOnClose: true
        });
    };

    /**
     * 확인 다이얼로그 (confirm 대체)
     * @param {string} message - 메시지
     * @param {Function} onConfirm - 확인 시 콜백
     * @param {string} title - 제목 (기본값: '확인')
     */
    window.showConfirm = function(message, onConfirm, title = '확인') {
        showCustomModal({
            title: title,
            content: `<p>${message}</p>`,
            buttons: [
                { text: '취소', class: 'btn-secondary', dismiss: true },
                {
                    text: '확인',
                    class: 'btn-primary',
                    onClick: function($modal) {
                        if (typeof onConfirm === 'function') {
                            onConfirm();
                        }
                        closeModal($modal.attr('id'));
                    }
                }
            ],
            removeOnClose: true
        });
    };

})();
