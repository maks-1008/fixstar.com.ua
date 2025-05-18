$(document).ready(function() {
    console.log('Modal cart script loaded');
    console.log('jQuery version:', $.fn.jquery);
    console.log('Bootstrap version:', typeof bootstrap !== 'undefined' ? bootstrap.Modal.VERSION : 'undefined');
    console.log('Document ready state:', document.readyState);
    
    // Проверяем наличие всех необходимых элементов на странице
    console.log('Modal button exists:', $('#modalButton').length > 0);
    console.log('Modal container exists:', $('#exampleModal').length > 0);
    console.log('Cart item container exists:', $('#cart-items-container').length > 0);
    
    // Проверяем, есть ли другие обработчики событий на кнопке модального окна
    if ($._data && $('#modalButton').length > 0) {
        console.log('Existing handlers on modal button:', $._data($('#modalButton')[0], 'events'));
    }
    
    // Указываем, что модальное окно открывается при клике на кнопку с идентификатором modalButton
    $('#modalButton').click(function() {
        // Обновляем содержимое корзины перед открытием модального окна
        // Событие открытия модального окна обрабатывается Bootstrap через data-атрибуты
        console.log('Cart button clicked, refreshing content');
        
        // Загружаем содержимое корзины через AJAX
        refreshCartModal();
        
        // Восстанавливаем все обработчики событий для элементов корзины
        if (window.initCartHandlers) {
            setTimeout(function() {
                window.initCartHandlers();
            }, 300);
        }
        
        console.log('Modal button click handler completed');
    });
    
    // Функция для обновления содержимого модального окна корзины
    function refreshCartModal() {
        console.log('==== REFRESH CART MODAL START ====');
        console.log('Modal container exists:', $('#exampleModal').length > 0);
        console.log('Modal body exists:', $('#exampleModal .modal-body').length > 0);
        console.log('Modal body container exists:', $('#exampleModal .modal-body .container').length > 0);
        console.log('Cart items container exists:', $('#cart-items-container').length > 0);
        console.log('Modal visible:', $('#exampleModal').hasClass('show'));
        
        // Выводим подробную информацию о DOM структуре модального окна
        if ($('#exampleModal').length > 0) {
            console.log('Modal DOM structure:', $('#exampleModal')[0].outerHTML.substring(0, 200) + '...');
            console.log('Modal body DOM structure:', $('#exampleModal .modal-body').length > 0 ? 
                        $('#exampleModal .modal-body')[0].outerHTML.substring(0, 200) + '...' : 'Not found');
        }
        
        // Если контейнера нет, пытаемся найти его другим способом
        const modalContainer = $('#exampleModal .modal-body .container');
        if (modalContainer.length === 0) {
            console.warn('Container not found by standard selector, trying alternative selectors');
            // Пробуем другие селекторы
            const alternativeContainers = [
                $('#exampleModal .modal-body #cart-items-container'),
                $('#exampleModal .modal-body div'),
                $('#cart-items-container')
            ];
            
            for (let i = 0; i < alternativeContainers.length; i++) {
                if (alternativeContainers[i].length > 0) {
                    console.log('Found alternative container:', i, alternativeContainers[i][0].outerHTML.substring(0, 100) + '...');
                    break;
                }
            }
        }
        
        console.log('Sending AJAX request to /cart/modal-content/');
        
        $.ajax({
            url: '/cart/modal-content/',  // Специальный URL для получения только содержимого корзины
            type: 'GET',
            dataType: 'html',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                console.log('Got response for cart modal, length:', response.length);
                console.log('Response sample:', response.substring(0, 100) + '...');
                
                // Проверяем все возможные контейнеры
                const containers = [
                    $('#exampleModal .modal-body .container'),
                    $('#exampleModal .modal-body #cart-items-container'),
                    $('#exampleModal #cart-items-container'),
                    $('#cart-items-container')
                ];
                
                console.log('Potential containers status:');
                for (let i = 0; i < containers.length; i++) {
                    console.log(`Container ${i}: ${containers[i].length > 0 ? 'Found' : 'Not found'}`);
                    if (containers[i].length > 0) {
                        console.log(`Container ${i} structure:`, containers[i][0].outerHTML.substring(0, 100) + '...');
                    }
                }
                
                let updated = false;
                for (let i = 0; i < containers.length; i++) {
                    if (containers[i].length > 0) {
                        console.log('Updating container:', i);
                        
                        try {
                            // Запоминаем старое содержимое для отладки
                            const oldHtml = containers[i].html();
                            console.log('Old container content length:', oldHtml.length);
                            
                            // Обновляем содержимое
                            containers[i].html(response);
                            
                            // Проверяем, что обновление произошло
                            const newHtml = containers[i].html();
                            console.log('New container content length:', newHtml.length);
                            console.log('Update successful:', oldHtml !== newHtml);
                            
                            updated = true;
                            break;
                        } catch (e) {
                            console.error('Error updating container:', e);
                        }
                    }
                }
                
                if (!updated) {
                    console.error('Could not find any valid container to update');
                    // Пробуем создать содержимое с нуля
                    try {
                        $('#exampleModal .modal-body').html('<div id="cart-items-container" class="container px-0">' + response + '</div>');
                        console.log('Created new container in modal body');
                        updated = true;
                    } catch (e) {
                        console.error('Error creating new container:', e);
                    }
                }
                
                // Переинициализируем обработчики событий
                if (window.initCartHandlers) {
                    console.log('Re-initializing cart handlers');
                    setTimeout(function() {
                        try {
                            window.initCartHandlers();
                            console.log('Cart handlers re-initialized successfully');
                        } catch (e) {
                            console.error('Error re-initializing handlers:', e);
                        }
                    }, 100);
                } else {
                    console.warn('initCartHandlers not available');
                }
                
                console.log('Cart modal content refreshed');
                
                // Триггерим событие, что контент обновлен
                $(document).trigger('cartModalRefreshed');
                console.log('cartModalRefreshed event triggered');
                
                console.log('==== REFRESH CART MODAL END ====');
            },
            error: function(xhr, status, error) {
                console.error('Error refreshing cart modal:', error);
                console.error('Status:', status);
                console.error('Response:', xhr.responseText);
                
                // Пробуем альтернативный подход через перезагрузку всего модального окна
                console.log('Trying alternative approach - reloading modal window');
                
                $('#exampleModal').modal('hide');
                setTimeout(function() {
                    location.reload();
                }, 500);
            }
        });
    }

    // Экспортируем функцию в глобальную область видимости
    window.refreshCartModal = refreshCartModal;
    
    // Обрабатываем событие показа модального окна
    $('#exampleModal').on('shown.bs.modal', function () {
        console.log('Modal shown event triggered');
        console.log('Modal is visible:', $(this).hasClass('show'));
        
        refreshCartModal();
        
        if (window.initCartHandlers) {
            try {
                window.initCartHandlers();
                console.log('Cart handlers initialized on modal shown');
            } catch (e) {
                console.error('Error initializing handlers on modal shown:', e);
            }
        }
    });
    
    // Обрабатываем событие обновления корзины
    $(document).on('cartUpdated', function(e, data) {
        console.log('Cart updated event received', data);
        // При обновлении корзины - обновляем счетчик и содержимое модального окна
        if (data && data.cart_count !== undefined) {
            $('#goods-in-cart-count').text(data.cart_count);
            console.log('Updated cart count to:', data.cart_count);
            
            // Также обновляем содержимое модального окна, если оно открыто
            if ($('#exampleModal').hasClass('show')) {
                console.log('Modal is open, refreshing content');
                refreshCartModal();
            } else {
                console.log('Modal is closed, not refreshing content');
            }
        }
    });
    
    // Выполняем первое обновление при загрузке страницы
    setTimeout(function() {
        console.log('Initial cart refresh');
        // Обновляем счетчик товаров в корзине
        $.ajax({
            url: '/cart/modal-content/',
            type: 'GET',
            dataType: 'html',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                // Парсим HTML для получения количества товаров
                try {
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = response;
                    const cartCount = $(tempDiv).find('#cart-items-count').text();
                    if (cartCount && cartCount.trim()) {
                        $('#goods-in-cart-count').text(cartCount);
                        console.log('Updated cart count on initial load:', cartCount);
                    } else {
                        console.warn('Could not find cart count in response');
                    }
                } catch (e) {
                    console.error('Error updating cart count on initial load:', e);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error in initial cart refresh:', error);
            }
        });
    }, 500);
    
    // Периодически проверяем и обновляем корзину, если она изменилась на стороне сервера
    setInterval(function() {
        console.log('Running periodic cart check');
        if (!$('#exampleModal').hasClass('show')) {
            $.ajax({
                url: '/cart/modal-content/',
                type: 'GET',
                dataType: 'html',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function(response) {
                    try {
                        const tempDiv = document.createElement('div');
                        tempDiv.innerHTML = response;
                        const cartCount = $(tempDiv).find('#cart-items-count').text();
                        if (cartCount && cartCount.trim()) {
                            const currentCount = $('#goods-in-cart-count').text();
                            if (cartCount !== currentCount) {
                                console.log('Cart count changed from server, updating from', currentCount, 'to', cartCount);
                                $('#goods-in-cart-count').text(cartCount);
                            }
                        }
                    } catch (e) {
                        console.error('Error in periodic cart check:', e);
                    }
                }
            });
        }
    }, 30000); // Проверка каждые 30 секунд
    
    console.log('Modal cart script initialization complete');
});

// Экспортируем функцию для обратной совместимости
if (typeof window.refreshCartModal === 'undefined' && typeof window.updateCartModal === 'function') {
    console.log('Setting refreshCartModal to updateCartModal for backward compatibility');
    window.refreshCartModal = window.updateCartModal;
}

// Добавляем возможность проверить состояние модуля в любой момент
window.debugModalCart = function() {
    console.log('Modal cart debug info:');
    console.log('Modal button exists:', $('#modalButton').length > 0);
    console.log('Modal container exists:', $('#exampleModal').length > 0);
    console.log('Modal is visible:', $('#exampleModal').hasClass('show'));
    console.log('Cart items container exists:', $('#cart-items-container').length > 0);
    console.log('refreshCartModal exists:', typeof window.refreshCartModal === 'function');
    console.log('updateCartModal exists:', typeof window.updateCartModal === 'function');
    console.log('initCartHandlers exists:', typeof window.initCartHandlers === 'function');
    
    if ($('#exampleModal').length > 0) {
        console.log('Modal DOM structure:', $('#exampleModal')[0].outerHTML.substring(0, 200) + '...');
    }
    
    if ($('#cart-items-container').length > 0) {
        console.log('Cart container DOM structure:', $('#cart-items-container')[0].outerHTML.substring(0, 200) + '...');
    }
};
