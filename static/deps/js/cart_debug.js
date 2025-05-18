/**
 * Функції для відлагодження корзини покупок
 * Файл містить допоміжні функції для виявлення проблем з корзиною
 */

(function() {
    // Інформація про ініціалізацію
    console.log('[cart-debug] Завантаження скрипту відлагодження корзини...');
    
    // Додаємо в глобальний об'єкт window функції відлагодження
    window.cartDebug = {
        // Функція перевірки стану корзини
        checkCartState: function() {
            console.group('Діагностика корзини покупок');
            console.log('Перевірка стану корзини...');
            
            // Перевірка елементів корзини
            const cartCountElement = document.getElementById('goods-in-cart-count');
            console.log('Елемент лічильника корзини:', cartCountElement ? 'Знайдено' : 'Не знайдено');
            console.log('Значення лічильника:', cartCountElement ? cartCountElement.textContent : 'N/A');
            
            // Перевірка модального вікна
            const cartModal = document.getElementById('exampleModal');
            console.log('Модальне вікно корзини:', cartModal ? 'Знайдено' : 'Не знайдено');
            console.log('Стан модального вікна:', cartModal ? (cartModal.classList.contains('show') ? 'Відкрито' : 'Закрито') : 'N/A');
            
            // Перевірка контенту корзини
            const cartContent = document.querySelector('.modal-body .cart-items-container');
            console.log('Контейнер товарів корзини:', cartContent ? 'Знайдено' : 'Не знайдено');
            
            if (cartContent) {
                const cartItems = cartContent.querySelectorAll('.cart-item');
                console.log('Кількість товарів в DOM:', cartItems.length);
                
                // Виведення інформації про кожен товар
                cartItems.forEach((item, index) => {
                    const titleElement = item.querySelector('.product-title');
                    const priceElement = item.querySelector('.price');
                    const quantityElement = item.querySelector('input[name="quantity"]');
                    
                    console.log(`Товар #${index + 1}:`, {
                        title: titleElement ? titleElement.textContent.trim() : 'Не знайдено',
                        price: priceElement ? priceElement.textContent.trim() : 'Не знайдено',
                        quantity: quantityElement ? quantityElement.value : 'Не знайдено'
                    });
                });
            }
            
            // Перевірка AJAX функцій
            console.log('refreshCartModal fn:', typeof window.refreshCartModal === 'function' ? 'Доступна' : 'Недоступна');
            console.log('initCartHandlers fn:', typeof window.initCartHandlers === 'function' ? 'Доступна' : 'Недоступна');
            
            console.groupEnd();
        },
        
        // Функція для тестової AJAX-запиту вмісту корзини
        testCartRequest: function() {
            console.log('[cart-debug] Запит даних корзини...');
            
            $.ajax({
                url: '/cart/modal-content/',
                type: 'GET',
                dataType: 'html',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function(response) {
                    console.log('[cart-debug] Успішна відповідь, довжина:', response.length);
                    
                    try {
                        const tempDiv = document.createElement('div');
                        tempDiv.innerHTML = response;
                        const cartCount = tempDiv.querySelector('#cart-items-count');
                        const cartItems = tempDiv.querySelectorAll('.cart-item');
                        
                        console.log('[cart-debug] Кількість товарів у відповіді:', cartItems.length);
                        console.log('[cart-debug] Лічильник у відповіді:', cartCount ? cartCount.textContent : 'Не знайдено');
                    } catch (error) {
                        console.error('[cart-debug] Помилка аналізу відповіді:', error);
                    }
                },
                error: function(xhr, status, error) {
                    console.error('[cart-debug] Помилка запиту корзини:', {
                        status: status,
                        error: error,
                        responseText: xhr.responseText ? xhr.responseText.substring(0, 100) + '...' : 'Пусто'
                    });
                }
            });
        },
        
        // Функція для оновлення корзини з детальним логуванням
        updateCartWithLogging: function() {
            console.log('[cart-debug] Спроба оновлення корзини...');
            
            if (typeof window.refreshCartModal === 'function') {
                console.log('[cart-debug] Виклик refreshCartModal...');
                try {
                    window.refreshCartModal(function(success) {
                        console.log('[cart-debug] Зворотній виклик refreshCartModal, успіх:', success);
                    });
                } catch (error) {
                    console.error('[cart-debug] Помилка при виклику refreshCartModal:', error);
                }
            } else {
                console.warn('[cart-debug] Функція refreshCartModal не знайдена!');
                
                // Спроба альтернативного оновлення
                this.testCartRequest();
            }
        }
    };
    
    // Ініціалізуємо слухачі подій
    document.addEventListener('DOMContentLoaded', function() {
        console.log('[cart-debug] DOM завантажено, ініціалізація відлагодження корзини...');
        
        // Додаємо обробник для подій корзини
        document.addEventListener('cartModalRefreshed', function(e) {
            console.log('[cart-debug] Подія cartModalRefreshed зафіксована:', e.detail);
        });
        
        document.addEventListener('cartUpdated', function(e) {
            console.log('[cart-debug] Подія cartUpdated зафіксована:', e.detail);
        });
        
        // Перевіряємо стан корзини через секунду після завантаження
        setTimeout(function() {
            window.cartDebug.checkCartState();
        }, 1000);
    });
    
    console.log('[cart-debug] Скрипт відлагодження корзини завантажено!');
})(); 