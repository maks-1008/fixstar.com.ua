document.addEventListener('DOMContentLoaded', function() {
    // Инициализация Toast
    const toastElement = document.getElementById('liveToast');
    const toast = toastElement ? new bootstrap.Toast(toastElement) : null;

    // Функция для показа уведомлений
    function showToast(message) {
        if (!toast) return;
        const toastBody = toastElement.querySelector('.toast-body');
        toastBody.textContent = message;
        toast.show();
        setTimeout(() => toast.hide(), 3000);
    }

    // Обработка всех форм добавления в корзину
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        const quantityInput = form.querySelector('input[name="quantity"]');
        const submitButton = form.querySelector('button[type="submit"]');
        const availabilityBadge = form.closest('tr').querySelector('.badge.bg-success');

        // Если товара нет в наличии - блокируем кнопку
        if (!availabilityBadge) {
            submitButton.disabled = true;
            submitButton.classList.add('disabled');
            return;
        }

        // Получаем доступное количество
        const availableQuantity = parseInt(availabilityBadge.dataset.availableQuantity) || 
                                parseInt(availabilityBadge.textContent.match(/\d+/)[0]) || 0;

        // Устанавливаем максимальное значение
        quantityInput.max = availableQuantity;

        // Валидация при изменении значения
        quantityInput.addEventListener('change', function() {
            let value = parseInt(this.value) || 1;
            if (value > availableQuantity) {
                this.value = availableQuantity;
                showToast(`Максимально доступно: ${availableQuantity} шт.`);
            } else if (value < 1) {
                this.value = 1;
            }
        });

        // Валидация перед отправкой формы
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const value = parseInt(quantityInput.value) || 1;
            
            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const data = await response.json();
                
                if (!response.ok || !data.success) {
                    throw new Error(data.message || 'Помилка сервера');
                }
                
                showToast(data.message || 'Товар додано до кошика');
                // Обновление корзины в UI (если нужно)
            } catch (error) {
                showToast(error.message);
                console.error('Error:', error);
            }
        });
    });
});