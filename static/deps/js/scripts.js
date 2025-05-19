// Основные JavaScript функции для сайта

document.addEventListener('DOMContentLoaded', function() {
    console.log('Document loaded, scripts initialized');
    
    // Инициализация всплывающих подсказок Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Инициализация модальных окон Bootstrap
    var modalTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="modal"]'));
    modalTriggerList.map(function (modalTriggerEl) {
        return new bootstrap.Modal(modalTriggerEl);
    });
    
    // Обработка событий клика для кнопок добавления в корзину
    setupAddToCartButtons();
    
    // Обработка событий для формы поиска
    setupSearchForm();
});

// Настройка кнопок добавления в корзину
function setupAddToCartButtons() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            
            // Анимация добавления в корзину
            this.classList.add('btn-success');
            this.innerHTML = '<i class="fas fa-check"></i> Добавлено';
            
            setTimeout(() => {
                this.classList.remove('btn-success');
                this.innerHTML = '<i class="fas fa-shopping-cart"></i> В корзину';
            }, 1500);
            
            // Здесь можно добавить AJAX-запрос для добавления товара в корзину
            console.log('Adding product to cart: ' + productId);
        });
    });
}

// Настройка формы поиска
function setupSearchForm() {
    const searchForm = document.querySelector('form[action*="search"]');
    if (!searchForm) return;
    
    searchForm.addEventListener('submit', function(e) {
        const searchInput = this.querySelector('input[name="q"]');
        if (searchInput && searchInput.value.trim() === '') {
            e.preventDefault();
            console.log('Empty search query');
        }
    });
}

// Функция для обновления содержимого корзины через AJAX
function refreshCart() {
    fetch('/cart/modal-content/')
        .then(response => response.text())
        .then(html => {
            const cartContainer = document.getElementById('cart-container');
            if (cartContainer) {
                cartContainer.innerHTML = html;
                
                // Обновление счетчика товаров в корзине
                const cartCounter = document.getElementById('cart-items-count');
                const cartBadge = document.getElementById('goods-in-cart-count');
                
                if (cartCounter && cartBadge) {
                    cartBadge.textContent = cartCounter.textContent;
                }
            }
        })
        .catch(error => console.error('Error updating cart:', error));
} 