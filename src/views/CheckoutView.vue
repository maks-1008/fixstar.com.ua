<script>
import { useCartStore } from '@/stores'
import { useOrderStore } from '@/stores'
import { useUserStore } from '@/stores'
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'CheckoutView',
  setup() {
    const cartStore = useCartStore()
    const orderStore = useOrderStore()
    const userStore = useUserStore()
    const router = useRouter()
    
    const cartItems = computed(() => cartStore.items)
    const totalItems = computed(() => cartStore.totalItems)
    const totalPrice = computed(() => cartStore.totalPrice)
    const isEmpty = computed(() => cartItems.value.length === 0)
    
    const formData = ref({
      firstName: userStore.user?.firstName || '',
      lastName: userStore.user?.lastName || '',
      email: userStore.user?.email || '',
      phone: userStore.user?.phone || '',
      requiresDelivery: true,
      deliveryAddress: '',
      paymentMethod: 'cash'
    })
    
    const paymentMethods = [
      { id: 'card', name: 'Оплата картою' },
      { id: 'cash', name: 'Готівкою/картою при отриманні' },
      { id: 'bank', name: 'Оплата на розрахунковий рахунок підприємства' }
    ]
    
    const isSubmitting = ref(false)
    const error = ref(null)
    
    const submitOrder = async () => {
      // Валидация формы
      if (!formData.value.firstName || !formData.value.lastName || !formData.value.phone) {
        error.value = 'Будь ласка, заповніть всі обов\'язкові поля'
        return
      }
      
      if (formData.value.requiresDelivery && !formData.value.deliveryAddress) {
        error.value = 'Будь ласка, вкажіть адресу доставки'
        return
      }
      
      isSubmitting.value = true
      error.value = null
      
      try {
        // Подготовка данных заказа
        const orderData = {
          ...formData.value,
          items: cartItems.value,
          total: totalPrice.value
        }
        
        // Отправка заказа
        const newOrder = await orderStore.createOrder(orderData)
        
        // Очистка корзины
        cartStore.clearCart()
        
        // Переход на страницу подтверждения заказа
        router.push({ 
          name: 'order', 
          params: { id: newOrder.id },
          query: { success: 'true' }
        })
      } catch (err) {
        error.value = 'Сталася помилка при оформленні замовлення. Спробуйте пізніше.'
        console.error(err)
      } finally {
        isSubmitting.value = false
      }
    }
    
    onMounted(() => {
      cartStore.loadCart()
      
      // Если корзина пуста, перенаправляем на страницу корзины
      if (cartStore.items.length === 0) {
        router.push({ name: 'cart' })
      }
    })
    
    return {
      cartItems,
      totalItems,
      totalPrice,
      isEmpty,
      formData,
      paymentMethods,
      isSubmitting,
      error,
      submitOrder
    }
  }
}
</script>

<template>
  <div class="checkout-view">
    <h1 class="mb-4">Оформлення замовлення</h1>
    
    <div v-if="!isEmpty">
      <div class="row">
        <!-- Форма оформления заказа -->
        <div class="col-lg-7 mb-4">
          <div class="card">
            <div class="card-header bg-dark text-white">
              <h5 class="mb-0">Інформація для замовлення</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="submitOrder">
                <!-- Сообщение об ошибке -->
                <div v-if="error" class="alert alert-danger" role="alert">
                  {{ error }}
                </div>
                
                <!-- Контактная информация -->
                <div class="mb-4">
                  <h6 class="mb-3">Контактна інформація</h6>
                  
                  <div class="row g-3">
                    <div class="col-md-6">
                      <label for="firstName" class="form-label">Ім'я *</label>
                      <input 
                        type="text" 
                        class="form-control" 
                        id="firstName" 
                        v-model="formData.firstName" 
                        required
                      >
                    </div>
                    <div class="col-md-6">
                      <label for="lastName" class="form-label">Прізвище *</label>
                      <input 
                        type="text" 
                        class="form-control" 
                        id="lastName" 
                        v-model="formData.lastName" 
                        required
                      >
                    </div>
                    <div class="col-md-6">
                      <label for="email" class="form-label">Email</label>
                      <input 
                        type="email" 
                        class="form-control" 
                        id="email" 
                        v-model="formData.email"
                      >
                    </div>
                    <div class="col-md-6">
                      <label for="phone" class="form-label">Телефон *</label>
                      <input 
                        type="tel" 
                        class="form-control" 
                        id="phone" 
                        v-model="formData.phone" 
                        required
                      >
                    </div>
                  </div>
                </div>
                
                <!-- Доставка -->
                <div class="mb-4">
                  <h6 class="mb-3">Доставка</h6>
                  
                  <div class="form-check mb-3">
                    <input 
                      class="form-check-input" 
                      type="checkbox" 
                      id="requiresDelivery" 
                      v-model="formData.requiresDelivery"
                    >
                    <label class="form-check-label" for="requiresDelivery">
                      Потрібна доставка
                    </label>
                  </div>
                  
                  <div v-if="formData.requiresDelivery" class="mb-3">
                    <label for="deliveryAddress" class="form-label">Адреса доставки *</label>
                    <textarea 
                      class="form-control" 
                      id="deliveryAddress" 
                      v-model="formData.deliveryAddress" 
                      rows="3"
                      required
                    ></textarea>
                  </div>
                </div>
                
                <!-- Оплата -->
                <div class="mb-4">
                  <h6 class="mb-3">Спосіб оплати</h6>
                  
                  <div class="mb-3">
                    <div v-for="method in paymentMethods" :key="method.id" class="form-check mb-2">
                      <input 
                        class="form-check-input" 
                        type="radio" 
                        :id="method.id" 
                        :value="method.id" 
                        v-model="formData.paymentMethod"
                      >
                      <label class="form-check-label" :for="method.id">
                        {{ method.name }}
                      </label>
                    </div>
                  </div>
                </div>
                
                <!-- Кнопки действий -->
                <div class="d-flex justify-content-between">
                  <router-link to="/cart" class="btn btn-outline-secondary">
                    <i class="bi bi-arrow-left me-2"></i>Повернутися до кошика
                  </router-link>
                  <button 
                    type="submit" 
                    class="btn btn-primary" 
                    :disabled="isSubmitting"
                  >
                    <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    <i v-else class="bi bi-check-circle me-2"></i>
                    Підтвердити замовлення
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
        
        <!-- Сводка заказа -->
        <div class="col-lg-5">
          <div class="card">
            <div class="card-header bg-dark text-white">
              <h5 class="mb-0">Ваше замовлення</h5>
            </div>
            <div class="card-body">
              <div class="order-summary">
                <div class="order-items mb-4">
                  <h6 class="mb-3">Товари ({{ totalItems }})</h6>
                  <div v-for="item in cartItems" :key="item.id" class="order-item mb-3">
                    <div class="d-flex justify-content-between">
                      <div>
                        <span class="item-name">{{ item.name }}</span>
                        <div class="text-muted small">{{ item.quantity }} x {{ item.price }} грн</div>
                      </div>
                      <div class="item-total">
                        {{ (item.quantity * item.price).toFixed(2) }} грн
                      </div>
                    </div>
                  </div>
                </div>
                
                <hr>
                
                <div class="order-total mb-3">
                  <div class="d-flex justify-content-between">
                    <span>Сума товарів:</span>
                    <span>{{ totalPrice.toFixed(2) }} грн</span>
                  </div>
                  <div class="d-flex justify-content-between">
                    <span>Доставка:</span>
                    <span>Безкоштовно</span>
                  </div>
                </div>
                
                <hr>
                
                <div class="final-total d-flex justify-content-between align-items-center">
                  <span class="fw-bold">Загальна сума:</span>
                  <span class="final-price">{{ totalPrice.toFixed(2) }} грн</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.checkout-view {
  padding-bottom: 30px;
}

.order-item {
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.order-item:last-child {
  border-bottom: none;
}

.item-name {
  font-weight: 500;
}

.item-total {
  font-weight: 500;
}

.final-price {
  font-size: 1.25rem;
  font-weight: 600;
  color: #ff6b00;
}
</style> 