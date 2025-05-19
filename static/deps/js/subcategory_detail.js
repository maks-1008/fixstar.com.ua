document.addEventListener('DOMContentLoaded', function() {
    console.log('Subcategory detail script initialized');
    
    // Глобальные переменные для отслеживания состояния
    let isFiltering = false;
    let originalScrollPosition = 0;
    let scrollLocked = false;
    let modalContentLoaded = false;
    let modalContentLoading = false;
    
    // Отладочная функция
    function debugLog(message) {
        console.log('[DEBUG] ' + message);
    }
    
    // Функция для блокировки скролла
    function lockScroll() {
        if (scrollLocked) return;
        
        originalScrollPosition = window.scrollY || window.pageYOffset;
        document.body.style.position = 'fixed';
        document.body.style.top = `-${originalScrollPosition}px`;
        document.body.style.width = '100%';
        document.body.classList.add('scroll-locked');
        
        scrollLocked = true;
        debugLog('Скролл заблокирован');
    }
    
    // Функция для разблокировки скролла
    function unlockScroll() {
        if (!scrollLocked) return;
        
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.width = '';
        document.body.classList.remove('scroll-locked');
        
        window.scrollTo(0, originalScrollPosition);
        scrollLocked = false;
        debugLog('Скролл разблокирован');
    }
    
    // Обработчик клика по фильтру
    function handleFilterClick(e) {
        e.preventDefault();
        e.stopPropagation();
        
        if (isFiltering) {
            debugLog('Фильтрация уже выполняется');
            return;
        }
        
        const link = e.currentTarget;
        const url = link.getAttribute('href');
        
        debugLog(`Клик по фильтру: ${url}`);
        
        // Блокируем скролл
        lockScroll();
        
        // Показываем оверлей загрузки
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay active';
        document.body.appendChild(overlay);
        
        // Делаем обычный переход
        window.location.href = url;
    }
    
    // Привязываем обработчики к фильтрам
    function attachFilterHandlers() {
        const filters = document.querySelectorAll('.filter-options a, .btn-filter');
        filters.forEach(filter => {
            filter.removeEventListener('click', handleFilterClick);
            filter.addEventListener('click', handleFilterClick);
        });
    }
    
    // Предотвращаем автоматическую прокрутку при загрузке
    window.addEventListener('load', function() {
        const hash = window.location.hash;
        if (hash) {
            window.location.hash = '';
        }
        
        // Разблокируем скролл
        unlockScroll();
    });
    
    // Инициализация
    attachFilterHandlers();
    
    // Функция для обновления фильтров длины
    function updateLengthFilters() {
        // Собираем текущие параметры фильтрации (кроме lengths)
        const params = new URLSearchParams(window.location.search);
        const activeFilters = {};
        
        // Добавляем только активные фильтры (кроме lengths)
        if (params.get('strength_class')) activeFilters.strength_class = params.get('strength_class');
        if (params.get('coating')) activeFilters.coating = params.get('coating');
        if (params.get('diameter')) activeFilters.diameter = params.get('diameter');
        
        // Если нет активных фильтров - показываем все варианты
        if (Object.keys(activeFilters).length === 0) {
            showAllLengthFilters();
            return;
        }
        
        // Формируем URL для AJAX запроса
        let queryString = Object.entries(activeFilters)
            .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
            .join('&');
        
        // Отправляем AJAX запрос для получения доступных длин
        fetch(`?${queryString}&get_lengths_only=1`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                updateLengthFiltersUI(data.lengths);
            })
            .catch(error => {
                console.error('Error fetching length filters:', error);
                showAllLengthFilters();
            });
    }
    
    // Функция для обновления UI фильтров длины (совместимая со всеми браузерами)
    function updateLengthFiltersUI(availableLengths) {
        // Найдем контейнер с фильтрами длины
        const lengthFilters = Array.from(document.querySelectorAll('.filter-group'));
        const lengthFilterGroup = lengthFilters.find(group => {
            const label = group.querySelector('.filter-label');
            return label && label.textContent.trim().includes('Довжина');
        });
        
        if (!lengthFilterGroup) return;
        
        const lengthLinks = lengthFilterGroup.querySelectorAll('.filter-options a');
        
        lengthLinks.forEach(link => {
            const lengthValue = link.textContent.trim();
            const isAvailable = availableLengths.includes(lengthValue);
            
            // Скрываем или показываем в зависимости от доступности
            link.style.display = isAvailable ? '' : 'none';
            
            // Если фильтр активен, но больше не доступен - деактивируем его
            if (link.classList.contains('active') && !isAvailable) {
                const newUrl = new URLSearchParams(window.location.search);
                newUrl.delete('lengths');
                window.history.replaceState({}, '', `${window.location.pathname}?${newUrl.toString()}`);
                link.classList.remove('active');
            }
        });
    }
    
    // Функция для показа всех фильтров длины (совместимая со всеми браузерами)
    function showAllLengthFilters() {
        // Найдем контейнер с фильтрами длины
        const lengthFilters = Array.from(document.querySelectorAll('.filter-group'));
        const lengthFilterGroup = lengthFilters.find(group => {
            const label = group.querySelector('.filter-label');
            return label && label.textContent.trim().includes('Довжина');
        });
        
        if (!lengthFilterGroup) return;
        
        lengthFilterGroup.querySelectorAll('.filter-options a').forEach(link => {
            link.style.display = '';
        });
    }
    
    // Обновляем фильтры длины при загрузке страницы
    try {
    updateLengthFilters();
    } catch(e) {
        console.error('Error in updateLengthFilters:', e);
    }
    
    // Обновляем фильтры длины при изменении URL (например, при нажатии кнопки "назад")
    window.addEventListener('popstate', function() {
        try {
            updateLengthFilters();
        } catch(e) {
            console.error('Error in popstate handler:', e);
        }
    });
    
    // Добавляем обработчики для всех фильтров (кроме lengths)
    try {
        const filterGroups = Array.from(document.querySelectorAll('.filter-group'));
        const nonLengthGroups = filterGroups.filter(group => {
            const label = group.querySelector('.filter-label');
            return label && !label.textContent.trim().includes('Довжина');
        });
        
        nonLengthGroups.forEach(group => {
            group.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function() {
            // Даем время для применения фильтра перед обновлением
            setTimeout(updateLengthFilters, 100);
        });
    });
        });
    } catch(e) {
        console.error('Error in filter click handlers:', e);
    }

    // Функция для обновления содержимого модального окна корзины
    function updateCartModal() {
        console.log('Updating cart modal content');
        
        try {
            // Получаем CSRF-токен из cookie
            const csrftoken = getCookie('csrftoken');
            
            // Отправляем запрос для получения обновленного содержимого корзины
            fetch('/cart/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) throw new Error('HTTP error ' + response.status);
                return response.text(); // Получаем HTML
            })
            .then(html => {
                // Создаем временный элемент для парсинга HTML
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = html;
                
                // Находим содержимое модальной корзины в полученном HTML
                const newCartContent = tempDiv.querySelector('#cart-items-container');
                
                if (newCartContent) {
                    // Находим все контейнеры корзины в текущем документе
                    const modalCartContainer = document.querySelector('#exampleModal #cart-items-container');
                    
                    if (modalCartContainer) {
                        console.log('Replacing modal cart content');
                        modalCartContainer.innerHTML = newCartContent.innerHTML;
                        
                        // Инициализируем обработчики в обновленном содержимом
                        if (typeof window.initCartHandlers === 'function') {
                            setTimeout(function() {
                                window.initCartHandlers();
                            }, 100);
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error updating cart modal:', error);
            });
        } catch(e) {
            console.error('Error in updateCartModal:', e);
        }
    }

    // AJAX обработка добавления товаров в корзину
    // Получаем CSRF-токен из cookie
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
        console.log('Showing notification:', message, 'isSuccess:', isSuccess);
        
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
        console.log('Updating cart counter to:', count);
        const counters = document.querySelectorAll('#goods-in-cart-count, #cart-items-count');
        counters.forEach(counter => {
            if (counter) counter.textContent = count;
        });
    }

    // Прямое перехватывание всех кликов на кнопки отправки формы добавления в корзину
    // Этот подход более надежен, чем использование addEventListener на форме
    try {
        console.log('Adding cart form interceptors');
        const forms = document.querySelectorAll('.add-to-cart-form');
        console.log('Found cart forms:', forms.length);
        
        // Устанавливаем обработчик для каждой формы
        forms.forEach(form => {
            // Заменяем стандартный обработчик отправки формы
            form.onsubmit = function(e) {
                e.preventDefault();
                console.log('Form submit intercepted');
                
                // Получаем CSRF-токен
                const csrftoken = getCookie('csrftoken');
                
                // Создаем объект FormData для сбора данных формы
                const formData = new FormData(form);
                
                // Показываем индикатор загрузки на кнопке
                const submitButton = form.querySelector('button[type="submit"]');
                const originalText = submitButton.innerHTML;
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Додаємо...';
                
                console.log('Sending AJAX request to:', form.action);
                
                // Отправляем AJAX запрос
                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken
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
                    console.log('Response received:', data);
                    
                    // Восстанавливаем кнопку
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalText;
                    
                    if (data.success) {
                        // Успешное добавление в корзину
                        showNotification(data.message, true);
                        
                        // Обновляем счетчик корзины, если есть данные
                        if (data.cart_count !== undefined) {
                            console.log('Updating cart counter to:', data.cart_count);
                            updateCartCounter(data.cart_count);
                            
                            // Явное обновление счетчика в кнопке корзины
                            $('#goods-in-cart-count').text(data.cart_count);
                        }
                        
                        // Обновляем содержимое модального окна корзины с выводом дополнительной информации
                        console.log('Attempting to refresh cart modal after adding item');
                        try {
                            // Проверяем, доступна ли функция обновления корзины в global scope
                            console.log('refreshCartModal exists:', typeof window.refreshCartModal === 'function');
                            
                            // Пробуем вызвать функцию
                            if (typeof window.refreshCartModal === 'function') {
                                window.refreshCartModal();
                                console.log('Called refreshCartModal successfully');
                            } else {
                                console.warn('refreshCartModal function not found in global scope');
                            }
                            
                            // Триггерим глобальное событие обновления корзины
                            console.log('Triggering cartUpdated event');
                            $(document).trigger('cartUpdated', data);
                            
                            // Пробуем вызвать обновление корзины напрямую через jQuery
                            console.log('Trying direct AJAX call to update cart');
    $.ajax({
                                url: '/cart/modal-content/',
        type: 'GET',
                                dataType: 'html',
                                headers: {
                                    'X-Requested-With': 'XMLHttpRequest'
                                },
        success: function(response) {
                                    console.log('Direct AJAX call success, length:', response.length);
                                    
                                    // Проверяем все возможные контейнеры
                                    const containers = [
                                        $('#exampleModal .modal-body .container'),
                                        $('#exampleModal .modal-body #cart-items-container'),
                                        $('#exampleModal #cart-items-container'),
                                        $('#cart-items-container')
                                    ];
                                    
                                    let updated = false;
                                    for (let i = 0; i < containers.length; i++) {
                                        if (containers[i].length > 0) {
                                            console.log('Direct update of container:', i);
                                            containers[i].html(response);
                                            updated = true;
                                            break;
                                        }
                                    }
                                    
                                    if (!updated) {
                                        console.error('Could not find any valid container for direct update');
                                    }
                                },
                                error: function(xhr, status, error) {
                                    console.error('Error in direct AJAX call:', error);
                                }
                            });
                        } catch (e) {
                            console.error('Error refreshing cart modal:', e);
                        }
                        
                        // Сбрасываем количество товара в форме до 1
                        form.querySelector('input[name="quantity"]').value = 1;
                    } else {
                        // Ошибка при добавлении
                        showNotification(data.message, false);
                    }
                })
                .catch(error => {
                    console.error('AJAX Error:', error);
                    
                    // Восстанавливаем кнопку
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalText;
                    
                    showNotification('Помилка при додаванні товару', false);
                });
                
                // Предотвращаем стандартную отправку формы
                return false;
            };
            
            // Также обрабатываем клики по кнопке отправки формы напрямую
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.onclick = function(e) {
                    // Предотвращаем клик по умолчанию
                    e.preventDefault();
                    // Отправляем событие submit на форму
                    form.onsubmit(e);
                    // Предотвращаем дальнейшую обработку
                    return false;
                };
            }
        });
    } catch(e) {
        console.error('Error setting up cart form handlers:', e);
    }
    
    // Экспортируем функцию для использования в других скриптах
    window.updateCartModal = updateCartModal;
});

// Обновляем определение функции обновления модального окна корзины для обратной совместимости
function updateCartModal() {
    console.log('Legacy updateCartModal called, using refreshCartModal instead');
    if (window.refreshCartModal) {
        window.refreshCartModal();
    }
}
