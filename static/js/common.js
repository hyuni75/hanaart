/* ========================================
   하나아트갤러리 공통 유틸리티 함수
   ======================================== */

(function() {
    'use strict';

    /**
     * CSRF 토큰 가져오기
     * @returns {string} CSRF 토큰
     */
    window.getCSRFToken = function() {
        return $('[name=csrfmiddlewaretoken]').val() || '';
    };

    /**
     * 폼 데이터를 FormData 객체로 변환
     * @param {string} formId - 폼 ID
     * @returns {FormData} FormData 객체
     */
    window.getFormData = function(formId) {
        const form = document.getElementById(formId);
        return new FormData(form);
    };

    /**
     * 날짜 포맷팅 (YYYY-MM-DD)
     * @param {Date|string} date - 날짜 객체 또는 문자열
     * @returns {string} 포맷된 날짜 문자열
     */
    window.formatDate = function(date) {
        if (!date) return '';
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    /**
     * 날짜 시간 포맷팅 (YYYY-MM-DD HH:MM)
     * @param {Date|string} datetime - 날짜시간 객체 또는 문자열
     * @returns {string} 포맷된 날짜시간 문자열
     */
    window.formatDateTime = function(datetime) {
        if (!datetime) return '';
        const d = new Date(datetime);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');
        return `${year}-${month}-${day} ${hours}:${minutes}`;
    };

    /**
     * 문자열 길이 제한 (말줄임표)
     * @param {string} str - 원본 문자열
     * @param {number} maxLength - 최대 길이
     * @returns {string} 잘린 문자열
     */
    window.truncateString = function(str, maxLength) {
        if (!str) return '';
        if (str.length <= maxLength) return str;
        return str.substring(0, maxLength) + '...';
    };

    /**
     * 숫자 포맷팅 (천단위 콤마)
     * @param {number} num - 숫자
     * @returns {string} 포맷된 숫자 문자열
     */
    window.formatNumber = function(num) {
        if (num === null || num === undefined) return '0';
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    };

    /**
     * 이미지 미리보기 생성
     * @param {File} file - 이미지 파일
     * @param {string} targetId - 미리보기를 표시할 요소 ID
     */
    window.previewImage = function(file, targetId) {
        if (!file || !file.type.startsWith('image/')) {
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            $(`#${targetId}`).html(`
                <div class="mt-2">
                    <p class="mb-2">미리보기:</p>
                    <img src="${e.target.result}" alt="미리보기"
                         style="max-height: 200px; max-width: 100%; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;">
                </div>
            `);
        };
        reader.readAsDataURL(file);
    };

    /**
     * 배열이 비어있는지 확인
     * @param {Array} arr - 배열
     * @returns {boolean}
     */
    window.isEmptyArray = function(arr) {
        return !arr || !Array.isArray(arr) || arr.length === 0;
    };

    /**
     * 객체가 비어있는지 확인
     * @param {Object} obj - 객체
     * @returns {boolean}
     */
    window.isEmptyObject = function(obj) {
        return !obj || Object.keys(obj).length === 0;
    };

    /**
     * URL 쿼리 파라미터 파싱
     * @returns {Object} 파라미터 객체
     */
    window.getQueryParams = function() {
        const params = {};
        const queryString = window.location.search.substring(1);
        const queries = queryString.split('&');

        queries.forEach(function(query) {
            const [key, value] = query.split('=');
            if (key) {
                params[decodeURIComponent(key)] = decodeURIComponent(value || '');
            }
        });

        return params;
    };

    /**
     * 페이지 새로고침
     */
    window.refreshPage = function() {
        window.location.reload();
    };

    /**
     * 페이지 이동
     * @param {string} url - 이동할 URL
     */
    window.navigateTo = function(url) {
        window.location.href = url;
    };

    /**
     * 콘솔 로그 래퍼 (개발 환경에서만 출력)
     * @param {...any} args - 로그 인자들
     */
    window.debugLog = function(...args) {
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            console.log('[DEBUG]', ...args);
        }
    };

    /**
     * 에러 로그 래퍼
     * @param {...any} args - 에러 인자들
     */
    window.errorLog = function(...args) {
        console.error('[ERROR]', ...args);
    };

})();
