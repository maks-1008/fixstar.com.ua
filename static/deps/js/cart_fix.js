/**
 * Файл для исправления поведения корзины - удаление диалогов подтверждения
 */
(function() {
    console.log('Cart fix script loaded');
    
    // Функция для переопределения обработчиков удаления
    function fixCartDeleteBehavior() {
        console.log('Fixing cart delete behavior - removing confirmation dialogs');
        
        // Находим все кнопки удаления в корзине
        const allDeleteButtons = document.querySelectorAll('.remove-from-cart, .session-remove-btn');
        console.log('Found delete buttons:', allDeleteButtons.length);
        
        // Перебираем кнопки и переопределяем их обработчики
        allDeleteButtons.forEach(function(button) {
            // Сначала удаляем существующие обработчики щелчка
            const oldClick = button.onclick;
            const oldHandlers = button.getEventListeners && button.getEventListeners('click');
            button.onclick = null;
            
            // Удаляем старые обработчики событий
            if (typeof jQuery !== 'undefined') {
                jQuery(button).off('click');
            }
            
            // Очищаем все существующие обработчики
            const newButton = button.cloneNode(true);
            button.parentNode.replaceChild(newButton, button);
            
            // Создаем новый обработчик без подтверждения
            if (newButton.classList.contains('remove-from-cart')) {
                // Для авторизованных пользователей
                newButton.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    const productId = this.getAttribute('data-product-id');
                    const url = this.getAttribute('href');
                    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                    
                    console.log("Direct removing product:", productId);
                    
                    fetch(url, {
                        method: 'POST',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': csrfToken
                        },
                        credentials: 'same-origin'
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            const row = newButton.closest('tr');
                            if (row) row.remove();
                            
                            // Обновляем счетчик и информацию о корзине
                            updateCartInfo(data);
                        } else {
                            showMessage(data.message || "Помилка при видаленні товару", false);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showMessage("Помилка при видаленні товару", false);
                    });
                });
            } else if (newButton.classList.contains('session-remove-btn')) {
                // Для сессионной корзины
                newButton.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    const productId = this.getAttribute('data-product-id');
                    if (!productId) return;
                    
                    console.log("Direct removing session product:", productId);
                    
                    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                    
                    fetch('/cart/session-remove/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': csrfToken
                        },
                        body: `product_id=${productId}`,
                        credentials: 'same-origin'
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            const row = newButton.closest('tr');
                            if (row) row.remove();
                            
                            // Обновляем счетчик и информацию о корзине
                            updateCartInfo(data);
                        } else {
                            showMessage(data.message || "Помилка при видаленні товару", false);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showMessage("Помилка при видаленні товару", false);
                    });
                });
            }
            
            console.log(`Added direct handler to button for product ID: ${newButton.getAttribute('data-product-id')}`);
        });
        
        console.log('Cart delete behavior fixed - confirmation dialogs removed');
    }
    
    // Вспомогательная функция для обновления информации о корзине
    function updateCartInfo(data) {
        console.log('Updating cart info with data:', data);
        
        // Обновляем счетчик товаров - количество категорий, а не общее количество
        if (data.cart_count !== undefined) {
            const counters = document.querySelectorAll('#goods-in-cart-count, #cart-items-count');
            counters.forEach(counter => {
                if (counter) counter.textContent = data.cart_count;
            });
        }
        
        // Обновляем общую сумму корзины
        if (data.cart_total !== undefined) {
            const totalElements = document.querySelectorAll('#cart-total-price');
            totalElements.forEach(element => {
                if (element) element.textContent = parseFloat(data.cart_total).toFixed(2);
            });
        }
        
        // Показываем сообщение об удалении
        if (data.message) {
            showMessage(data.message, true);
        }
        
        // Вызываем событие обновления корзины
        if (typeof jQuery !== 'undefined') {
            jQuery(document).trigger('cartUpdated', data);
        }
    }
    
    // Функция для отображения уведомлений
    function showMessage(message, isSuccess) {
        // Создаем элемент уведомления
        const notification = document.createElement('div');
        notification.className = 'cart-notification ' + (isSuccess ? 'success' : 'error');
        notification.textContent = message;
        notification.style.position = 'fixed';
        notification.style.bottom = '20px';
        notification.style.right = '20px';
        notification.style.padding = '10px 20px';
        notification.style.backgroundColor = isSuccess ? '#28a745' : '#dc3545';
        notification.style.color = 'white';
        notification.style.borderRadius = '4px';
        notification.style.zIndex = '9999';
        notification.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
        
        // Добавляем уведомление в DOM
        document.body.appendChild(notification);
        
        // Удаляем уведомление через 3 секунды
        setTimeout(function() {
            notification.style.opacity = '0';
            notification.style.transition = 'opacity 0.5s';
            setTimeout(function() {
                document.body.removeChild(notification);
            }, 500);
        }, 3000);
    }
    
    // Выполняем исправление при загрузке DOM
    document.addEventListener('DOMContentLoaded', function() {
        console.log('DOM loaded, will fix cart behavior');
        fixCartDeleteBehavior();
    });
    
    // Также запускаем исправление через setTimeout для случаев, когда корзина загружается динамически
    setTimeout(function() {
        console.log('Timeout elapsed, fixing cart behavior again');
        fixCartDeleteBehavior();
    }, 1000);
    
    // Обрабатываем событие обновления корзины
    if (typeof jQuery !== 'undefined') {
        jQuery(document).on('cartModalRefreshed', function() {
            console.log('Cart modal refreshed, fixing delete behavior');
            setTimeout(fixCartDeleteBehavior, 100);
        });
    }
})(); 