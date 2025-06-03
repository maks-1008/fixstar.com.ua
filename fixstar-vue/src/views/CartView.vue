<script>
import { useCartStore } from '@/stores'
import { onMounted, computed } from 'vue'

export default {
  name: 'CartView',
  setup() {
    const cartStore = useCartStore()
    
    const cartItems = computed(() => cartStore.items)
    const totalItems = computed(() => cartStore.totalItems)
    const totalPrice = computed(() => cartStore.totalPrice)
    const isEmpty = computed(() => cartItems.value.length === 0)
    
    const removeItem = (id) => {
      if (confirm('Ви впевнені, що хочете видалити цей товар з кошика?')) {
        cartStore.removeFromCart(id)
      }
    }
    
    const updateQuantity = (id, quantity) => {
      if (quantity < 1) quantity = 1
      cartStore.updateQuantity(id, quantity)
    }
    
    const clearCart = () => {
      if (confirm('Ви впевнені, що хочете очистити кошик?')) {
        cartStore.clearCart()
      }
    }
    
    onMounted(() => {
      cartStore.loadCart()
    })
    
    return {
      cartItems,
      totalItems,
      totalPrice,
      isEmpty,
      removeItem,
      updateQuantity,
      clearCart
    }
  }
}
</script>

<template>
  <div class="cart-view">
    <h1 class="mb-4">Кошик</h1>
    
    <!-- Пустая корзина -->
    <div v-if="isEmpty" class="empty-cart text-center my-5">
      <i class="bi bi-cart-x display-1 text-muted"></i>
      <h3 class="mt-3">Ваш кошик порожній</h3>
      <p class="text-muted mb-4">Додайте товари до кошика, щоб продовжити покупки.</p>
      <router-link to="/catalog" class="btn btn-primary">
        <i class="bi bi-shop me-2"></i>Перейти до каталогу
      </router-link>
    </div>
    
    <!-- Содержимое корзины -->
    <div v-else>
      <div class="card mb-4">
        <div class="card-header bg-dark text-white">
          <div class="d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Ваші товари ({{ totalItems }})</h5>
            <button @click="clearCart" class="btn btn-sm btn-outline-light">
              <i class="bi bi-trash me-1"></i>Очистити кошик
            </button>
          </div>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover table-bordered m-0">
              <thead class="table-light">
                <tr>
                  <th scope="col">Товар</th>
                  <th scope="col" class="text-center" style="width: 120px;">Ціна</th>
                  <th scope="col" class="text-center" style="width: 150px;">Кількість</th>
                  <th scope="col" class="text-center" style="width: 120px;">Сума</th>
                  <th scope="col" class="text-center" style="width: 80px;">Дія</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in cartItems" :key="item.id">
                  <td>
                    <div class="d-flex align-items-center">
                      <div class="cart-item-img me-3">
                        <img 
                          v-if="item.image" 
                          :src="item.image" 
                          :alt="item.name" 
                          class="img-thumbnail"
                        >
                        <i v-else class="bi bi-box cart-item-icon"></i>
                      </div>
                      <div>
                        <h6 class="mb-0">{{ item.name }}</h6>
                      </div>
                    </div>
                  </td>
                  <td class="text-center align-middle">{{ item.price }} грн</td>
                  <td class="text-center align-middle">
                    <div class="input-group input-group-sm">
                      <button 
                        class="btn btn-outline-secondary" 
                        type="button"
                        @click="updateQuantity(item.id, item.quantity - 1)"
                      >-</button>
                      <input 
                        type="number" 
                        class="form-control text-center" 
                        :value="item.quantity"
                        @change="updateQuantity(item.id, parseInt($event.target.value))"
                        min="1"
                      >
                      <button 
                        class="btn btn-outline-secondary" 
                        type="button"
                        @click="updateQuantity(item.id, item.quantity + 1)"
                      >+</button>
                    </div>
                  </td>
                  <td class="text-center align-middle fw-bold">{{ (item.price * item.quantity).toFixed(2) }} грн</td>
                  <td class="text-center align-middle">
                    <button 
                      @click="removeItem(item.id)" 
                      class="btn btn-sm btn-outline-danger"
                      title="Видалити"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
              <tfoot class="table-light">
                <tr>
                  <td colspan="3" class="text-end fw-bold">Загальна сума:</td>
                  <td class="text-center fw-bold price-text">{{ totalPrice.toFixed(2) }} грн</td>
                  <td></td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
      </div>
      
      <!-- Кнопки действий -->
      <div class="d-flex justify-content-between">
        <router-link to="/catalog" class="btn btn-outline-secondary">
          <i class="bi bi-arrow-left me-2"></i>Продовжити покупки
        </router-link>
        <router-link to="/checkout" class="btn btn-primary">
          <i class="bi bi-credit-card me-2"></i>Оформити замовлення
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cart-view {
  padding-bottom: 30px;
}

.cart-item-img {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
}

.cart-item-img img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.cart-item-icon {
  font-size: 2rem;
  color: #6c757d;
}

.price-text {
  color: #ff6b00;
}

/* Предотвращение стрелок в input number */
input[type=number]::-webkit-inner-spin-button, 
input[type=number]::-webkit-outer-spin-button { 
  -webkit-appearance: none; 
  margin: 0; 
}
input[type=number] {
  -moz-appearance: textfield;
}
</style> 