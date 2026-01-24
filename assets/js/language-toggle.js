/**
 * Bilingual Language Toggle Component
 * Switches between Korean (KO) and English (EN) for all bilingual text elements
 */
(function() {
    'use strict';

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        const toggleBtn = document.getElementById('lang-toggle');
        if (!toggleBtn) return; // Exit if toggle button doesn't exist

        const langOptions = toggleBtn.querySelectorAll('.lang-option');
        let currentLang = loadSavedLanguage() || 'ko'; // Default to Korean

        // Set initial language if not Korean
        if (currentLang === 'en') {
            setLanguage('en', langOptions);
        }

        // Add click event listener
        toggleBtn.addEventListener('click', function() {
            currentLang = currentLang === 'ko' ? 'en' : 'ko';
            setLanguage(currentLang, langOptions);
            saveLanguagePreference(currentLang);
        });
    }

    /**
     * Set the language for all bilingual elements
     */
    function setLanguage(lang, langOptions) {
        // Update toggle button visual
        langOptions.forEach(option => {
            if (option.classList.contains(`lang-${lang}`)) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });

        // Update all bilingual text elements
        document.querySelectorAll('.bilingual-text').forEach(element => {
            const text = element.getAttribute(`data-${lang}`);
            if (text) {
                // Add fade effect
                element.style.opacity = '0';

                setTimeout(() => {
                    element.textContent = text;
                    element.style.opacity = '1';
                }, 150);
            }
        });
    }

    /**
     * Save language preference to localStorage
     */
    function saveLanguagePreference(lang) {
        try {
            localStorage.setItem('preferredLanguage', lang);
        } catch (e) {
            console.warn('Unable to save language preference:', e);
        }
    }

    /**
     * Load saved language preference from localStorage
     */
    function loadSavedLanguage() {
        try {
            return localStorage.getItem('preferredLanguage');
        } catch (e) {
            console.warn('Unable to load language preference:', e);
            return null;
        }
    }
})();
