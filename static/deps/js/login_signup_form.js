/**
 * Скрипт для форм входа и регистрации
 */
(function() {
    // Получаем контейнер
    const container = document.querySelector('.login-signup-container');
    if (!container) return;
    
    // Проверяем значение data-active-form
    const activeForm = container.getAttribute('data-active-form');
    
    // Устанавливаем правильный класс в зависимости от активной формы
    if (activeForm === 'signup') {
        container.classList.add('signup-mode');
    } else {
        container.classList.remove('signup-mode');
    }
    
    // Получаем кнопки переключения
    const showLoginBtn = document.querySelector('#show-login');
    const showSignupBtn = document.querySelector('#show-signup');

    // Обработчик для перехода к форме регистрации
    if (showSignupBtn) {
        showSignupBtn.addEventListener('click', function(e) {
            e.preventDefault();
            container.classList.add('signup-mode');
            
            // Фокус на поле ввода формы регистрации после анимации
            setTimeout(function() {
                const usernameField = document.querySelector('#id_signup_username');
                if (usernameField) {
                    usernameField.focus();
                }
            }, 600);
        });
    }
    
    // Обработчик для возврата к форме входа
    if (showLoginBtn) {
        showLoginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            container.classList.remove('signup-mode');
            
            // Фокус на поле ввода формы входа после анимации
            setTimeout(function() {
                const usernameField = document.querySelector('#id_username');
                if (usernameField) {
                    usernameField.focus();
                }
            }, 600);
        });
    }
})(); 