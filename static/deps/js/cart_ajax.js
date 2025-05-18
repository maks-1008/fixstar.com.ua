document.addEventListener('DOMContentLoaded', function() {
    // Получаем CSRF-токен один раз при загрузке страницы
    let csrfToken = getCookie('csrftoken');
    
    // Функция для получения CSRF-токена из cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Функция для отображения уведомлений
    function showNotification(message, isSuccess) {
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
    
    // Функция для обновления счетчика товаров в корзине
    function updateCartCounter(count) {
        const counters = document.querySelectorAll('#goods-in-cart-count, #cart-items-count');
        counters.forEach(counter => {
            if (counter) counter.textContent = count;
        });
        
        // Вызываем событие для уведомления о изменении корзины
        triggerCartUpdatedEvent({ cart_count: count });
    }
    
    // Функция для генерации события обновления корзины
    function triggerCartUpdatedEvent(data) {
        // Проверяем доступность jQuery
        if (typeof jQuery !== 'undefined') {
            jQuery(document).trigger('cartUpdated', data);
        }
    }
    
    // Функция для обновления цен в корзине
    function updateCartPrices(itemPrice, cartTotal, rowElement) {
        // Обновляем цену позиции
        if (rowElement && itemPrice) {
            const priceCell = rowElement.querySelector('.item-total-price');
            if (priceCell) {
                // Анимация обновления цены
                const oldPrice = priceCell.textContent.replace(/[^\d.]/g, '');
                const newPrice = itemPrice.toString().replace(/[^\d.]/g, '');
                
                if (oldPrice !== newPrice) {
                    // Определяем направление изменения цены
                    const isIncrease = parseFloat(newPrice) > parseFloat(oldPrice);
                    
                    // Применяем анимацию
                    priceCell.style.transition = 'transform 0.3s, color 0.3s';
                    priceCell.style.color = isIncrease ? '#ff5722' : '#4caf50';
                    priceCell.style.transform = 'scale(1.1)';
                    
                    // Устанавливаем новое значение
                    priceCell.innerHTML = `${itemPrice} грн`;
                    
                    // Возвращаем стиль к нормальному
                    setTimeout(function() {
                        priceCell.style.transform = 'scale(1)';
                        setTimeout(function() {
                            priceCell.style.color = '';
                        }, 300);
                    }, 300);
                } else {
                    priceCell.innerHTML = `${itemPrice} грн`;
                }
            }
        }
        
        // Обновляем общую сумму корзины
        if (cartTotal) {
            const totalElements = document.querySelectorAll('#cart-total-price');
            totalElements.forEach(element => {
                if (element) {
                    const oldTotal = element.textContent.replace(/[^\d.]/g, '');
                    const newTotal = cartTotal.toString().replace(/[^\d.]/g, '');
                    
                    if (oldTotal !== newTotal) {
                        // Анимация изменения
                        element.style.transition = 'transform 0.5s, color 0.5s';
                        element.style.color = '#ff9800';
                        element.style.transform = 'scale(1.1)';
                        
                        element.textContent = cartTotal;
                        
                        setTimeout(function() {
                            element.style.transform = 'scale(1)';
                            setTimeout(function() {
                                element.style.color = '';
                            }, 500);
                        }, 500);
                    } else {
                        element.textContent = cartTotal;
                    }
                }
            });
        }
        
        // Вызываем событие при обновлении цен
        if (cartTotal) {
            triggerCartUpdatedEvent({ cart_total: cartTotal });
        }
    }
    
    // Находим все формы добавления в корзину
    const cartForms = document.querySelectorAll('.add-to-cart-form');
    
    // Добавляем обработчик отправки формы для каждой формы
    cartForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            // Предотвращаем стандартную отправку формы
            e.preventDefault();
            
            // Создаем объект FormData для сбора данных формы
            const formData = new FormData(form);
            
            // Отправляем AJAX запрос
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('HTTP error ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Успешное добавление в корзину
                    showNotification(data.message, true);
                    
                    // Обновляем счетчик корзины, если есть данные
                    if (data.cart_count !== undefined) {
                        updateCartCounter(data.cart_count);
                    }
                    
                    // Вызываем событие с полными данными
                    triggerCartUpdatedEvent(data);
                } else {
                    // Ошибка при добавлении
                    showNotification(data.message, false);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Произошла ошибка при добавлении товара', false);
            });
        });
    });
    
    // Инициализируем все обработчики событий корзины
    function initCartHandlers() {
        console.log('Initializing cart handlers');
        
        // Обработка изменения количества товара в корзине через input type="number"
        const quantityInputs = document.querySelectorAll('.cart-quantity-input');
        quantityInputs.forEach(function(input) {
            // Удаляем существующий обработчик, чтобы избежать дублирования
            input.removeEventListener('change', handleQuantityChange);
            
            // Сохраняем исходное значение при фокусе для отмены при ошибке
            let originalValue;
            input.addEventListener('focus', function() {
                originalValue = this.value;
            });
            
            // Добавляем обработчик события
            input.addEventListener('change', handleQuantityChange);
            
            // Функция обработки изменения количества
            function handleQuantityChange() {
                console.log('Quantity changed:', input.value);
                
                let value = parseInt(input.value);
                if (isNaN(value) || value < 1) {
                    value = 1;
                    input.value = 1;
                    showNotification("Кількість не може бути менше 1", false);
                    return;
                }
                
                const parentRow = input.closest('tr');
                
                // Получаем данные для запроса
                const productId = input.getAttribute('data-product-id');
                const cartId = input.getAttribute('data-cart-id');
                const changeUrl = input.getAttribute('data-cart-change-url');
                
                if (!changeUrl) {
                    console.error('URL для изменения не найден');
                    return;
                }
                
                // Подготавливаем данные для отправки
                const formData = new FormData();
                if (cartId) formData.append('cart_id', cartId);
                if (productId) formData.append('product_id', productId);
                formData.append('quantity', value);
                
                // Показываем индикатор загрузки
                input.disabled = true;
                input.style.opacity = '0.5';
                
                // Отладочная информация
                console.log('Sending request to:', changeUrl);
                console.log('With data:', {
                    cart_id: cartId,
                    product_id: productId,
                    quantity: value
                });
                
                // Отправляем запрос
                fetch(changeUrl, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken
                    },
                    credentials: 'same-origin'
                })
                .then(response => {
                    console.log('Response status:', response.status);
                    if (!response.ok) {
                        throw new Error('HTTP error ' + response.status);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Response data:', data);
                    
                    // Восстанавливаем поле ввода
                    input.style.opacity = '1';
                    input.disabled = false;
                    
                    if (data.success) {
                        // Обновляем цены в корзине
                        updateCartPrices(data.item_price, data.cart_total, parentRow);
                        
                        // Обновляем счетчик товаров
                        if (data.cart_count !== undefined) {
                            updateCartCounter(data.cart_count);
                        }
                        
                        // Вызываем событие с полными данными
                        triggerCartUpdatedEvent(data);
                        
                        // Показываем сообщение об успехе
                        showNotification(data.message || "Кількість товару змінено", true);
                    } else {
                        // Восстанавливаем исходное значение при ошибке
                        input.value = originalValue || 1;
                        showNotification(data.message || 'Помилка при зміні кількості', false);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Восстанавливаем поле ввода и исходное значение
                    input.style.opacity = '1';
                    input.disabled = false;
                    input.value = originalValue || 1;
                    showNotification('Сталася помилка при зміні кількості товару', false);
                });
            }
        });
        
        // Обработка удаления товара для авторизованных пользователей
        const removeButtons = document.querySelectorAll('.remove-from-cart');
        removeButtons.forEach(function(button) {
            // Удаляем существующий обработчик
            button.removeEventListener('click', handleRemoveClick);
            
            // Добавляем новый обработчик
            button.addEventListener('click', handleRemoveClick);
            
            function handleRemoveClick(e) {
                e.preventDefault();
                
                if (!confirm('Ви дійсно хочете видалити цей товар з кошика?')) {
                    return;
                }
                
                const productId = button.getAttribute('data-product-id');
                const url = button.getAttribute('href');
                
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken
                    },
                    credentials: 'same-origin'
                })
                .then(response => {
                    if (!response.ok) throw new Error('HTTP Error ' + response.status);
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        const row = button.closest('tr');
                        if (row) row.remove();
                        showNotification(data.message || "Товар видалено з кошика", true);
                        updateCartCounter(data.cart_count);
                        updateCartPrices(null, data.cart_total, null);
                        
                        // Проверяем, пустая ли корзина
                        if (data.cart_count === 0) {
                            const tbody = document.querySelector('.product-table tbody');
                            if (tbody) {
                                tbody.innerHTML = '<tr><td colspan="6" class="text-center">Кошик порожній</td></tr>';
                            }
                        }
                    } else {
                        showNotification(data.message || "Помилка при видаленні товару", false);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showNotification("Помилка при видаленні товару", false);
                });
            }
        });
        
        // Обработка удаления товаров из сессионной корзины
        const sessionRemoveButtons = document.querySelectorAll('.session-remove-btn');
        sessionRemoveButtons.forEach(function(button) {
            // Удаляем существующий обработчик
            button.removeEventListener('click', handleSessionRemoveClick);
            
            // Добавляем новый обработчик
            button.addEventListener('click', handleSessionRemoveClick);
            
            function handleSessionRemoveClick(e) {
                e.preventDefault();
                
                if (!confirm('Ви дійсно хочете видалити цей товар з кошика?')) {
                    return;
                }
                
                const productId = button.getAttribute('data-product-id');
                if (!productId) return;
                
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
                .then(response => {
                    if (!response.ok) throw new Error('HTTP Error ' + response.status);
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        const row = button.closest('tr');
                        if (row) row.remove();
                        showNotification(data.message || "Товар видалено з кошика", true);
                        updateCartCounter(data.cart_count);
                        updateCartPrices(null, data.cart_total, null);
                        
                        // Проверяем, пустая ли корзина
                        if (data.cart_count === 0) {
                            const tbody = document.querySelector('.product-table tbody');
                            if (tbody) {
                                tbody.innerHTML = '<tr><td colspan="6" class="text-center">Кошик порожній</td></tr>';
                            }
                        }
                    } else {
                        showNotification(data.message || "Помилка при видаленні товару", false);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showNotification("Помилка при видаленні товару", false);
                });
            }
        });
    }
    
    // Инициализируем обработчики при загрузке страницы
    initCartHandlers();
    
    // Запускаем инициализацию обработчиков при получении события обновления корзины
    if (typeof jQuery !== 'undefined') {
        jQuery(document).on('cartUpdated', function() {
            // Даем время на обновление DOM
            setTimeout(initCartHandlers, 100);
        });
    }
    
    // Экспортируем функцию для использования в других скриптах
    window.initCartHandlers = initCartHandlers;
});
