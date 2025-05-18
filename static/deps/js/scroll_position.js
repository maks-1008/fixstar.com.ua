// Функция для сохранения точной позиции прокрутки перед отправкой формы
document.addEventListener('DOMContentLoaded', function() {
    // Используем более стабильное хранилище - sessionStorage вместо localStorage
    // sessionStorage очищается при закрытии вкладки
    
    // Восстанавливаем позицию прокрутки, если она была сохранена
    function restoreScrollPosition() {
        const scrollY = sessionStorage.getItem('exactScrollY');
        if (scrollY) {
            // Устанавливаем таймаут, чтобы дать странице полностью загрузиться
            setTimeout(function() {
                window.scrollTo(0, parseInt(scrollY));
                // Удаляем сохраненное значение после восстановления
                sessionStorage.removeItem('exactScrollY');
            }, 0);
        }
    }
    
    // Добавляем обработчики всем формам добавления в корзину
    const forms = document.querySelectorAll('.add-to-cart-form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            // Сохраняем текущую точную позицию прокрутки
            sessionStorage.setItem('exactScrollY', window.pageYOffset.toString());
        });
    });
    
    // Восстанавливаем позицию прокрутки при загрузке страницы
    // Используем событие 'load', которое срабатывает после полной загрузки всех ресурсов
    if (document.readyState === 'complete') {
        restoreScrollPosition();
    } else {
        window.addEventListener('load', restoreScrollPosition);
    }
});