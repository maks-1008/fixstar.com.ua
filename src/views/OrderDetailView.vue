<script>
import { useOrderStore } from '@/stores'
import { useUserStore } from '@/stores'
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'OrderDetailView',
  setup() {
    const orderStore = useOrderStore()
    const userStore = useUserStore()
    const route = useRoute()
    const router = useRouter()
    
    const orderId = computed(() => route.params.id)
    const isSuccess = computed(() => route.query.success === 'true')
    
    const order = computed(() => {
      return orderStore.getOrderById(orderId.value)
    })
    
    const isLoading = ref(true)
    const error = ref(null)
    
    // Форматирование даты
    const formatDate = (dateString) => {
      const options = { day: 'numeric', month: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric' }
      return new Date(dateString).toLocaleString('uk-UA', options)
    }
    
    // Получение класса для статуса заказа
    const getStatusClass = (status) => {
      switch (status) {
        case 'CREATED':
          return 'bg-secondary'
        case 'PAID':
          return 'bg-primary'
        case 'ON_WAY':
          return 'bg-info'
        case 'DELIVERED':
          return 'bg-success'
        case 'CANCELED':
          return 'bg-danger'
        default:
          return 'bg-secondary'
      }
    }
    
    // Получение текста статуса заказа
    const getStatusText = (status) => {
      switch (status) {
        case 'CREATED':
          return 'Створено'
        case 'PAID':
          return 'Оплачено'
        case 'ON_WAY':
          return 'В дорозі'
        case 'DELIVERED':
          return 'Доставлено'
        case 'CANCELED':
          return 'Скасовано'
        default:
          return 'Невідомо'
      }
    }
    
    onMounted(async () => {
      // Проверка авторизации
      if (!userStore.isAuthenticated) {
        router.push({ name: 'login', query: { redirect: `/order/${orderId.value}` } })
        return
      }
      
      try {
        isLoading.value = true
        
        // Если заказов нет, загружаем их
        if (orderStore.orders.length === 0) {
          await orderStore.fetchOrders(userStore.user.id)
        }
        
        // Если заказ не найден даже после загрузки, показываем ошибку
        if (!order.value) {
          error.value = 'Замовлення не знайдено'
        }
      } catch (err) {
        error.value = 'Помилка при завантаженні замовлення'
        console.error(err)
      } finally {
        isLoading.value = false
      }
    })
    
    return {
      order,
      isLoading,
      error,
      isSuccess,
      formatDate,
      getStatusClass,
      getStatusText
    }
  }
}
</script>

<template>
  <div class="order-detail-view">
    <h1 class="mb-4">Деталі замовлення</h1>
    
    <!-- Сообщение об успешном создании заказа -->
    <div v-if="isSuccess && order" class="alert alert-success mb-4" role="alert">
      <h4 class="alert-heading">Дякуємо за ваше замовлення!</h4>
      <p>Замовлення №{{ order.id }} успішно оформлено.</p>
      <p class="mb-0">Ми зв'яжемося з вами найближчим часом для підтвердження замовлення.</p>
    </div>
    
    <!-- Загрузка -->
    <div v-if="isLoading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Завантаження...</span>
      </div>
      <p class="mt-2">Завантаження деталей замовлення...</p>
    </div>
    
    <!-- Ошибка -->
    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
      <div class="mt-3">
        <router-link to="/orders" class="btn btn-outline-primary btn-sm">
          <i class="bi bi-arrow-left me-1"></i>Повернутися до списку замовлень
        </router-link>
      </div>
    </div>
    
    <!-- Детали заказа -->
    <div v-else-if="order" class="row">
      <div class="col-lg-8">
        <!-- Основная информация о заказе -->
        <div class="card mb-4">
          <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Замовлення № {{ order.id }}</h5>
            <span :class="['badge', getStatusClass(order.status)]">
              {{ getStatusText(order.status) }}
            </span>
          </div>
          <div class="card-body">
            <div class="order-info mb-4">
              <div class="row mb-2">
                <div class="col-md-4 text-muted">Дата створення:</div>
                <div class="col-md-8">{{ formatDate(order.created_at) }}</div>
              </div>
              <div class="row mb-2">
                <div class="col-md-4 text-muted">Статус:</div>
                <div class="col-md-8">
                  <span :class="['badge', getStatusClass(order.status)]">
                    {{ getStatusText(order.status) }}
                  </span>
                </div>
              </div>
              <div class="row">
                <div class="col-md-4 text-muted">Загальна сума:</div>
                <div class="col-md-8 fw-bold price-text">{{ order.total.toFixed(2) }} грн</div>
              </div>
            </div>
            
            <h6 class="mb-3">Товари у замовленні:</h6>
            <div class="table-responsive">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>Товар</th>
                    <th class="text-center">Ціна</th>
                    <th class="text-center">Кількість</th>
                    <th class="text-end">Сума</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in order.items" :key="item.id">
                    <td>{{ item.name }}</td>
                    <td class="text-center">{{ item.price.toFixed(2) }} грн</td>
                    <td class="text-center">{{ item.quantity }}</td>
                    <td class="text-end">{{ (item.price * item.quantity).toFixed(2) }} грн</td>
                  </tr>
                </tbody>
                <tfoot>
                  <tr>
                    <td colspan="3" class="text-end fw-bold">Загальна сума:</td>
                    <td class="text-end fw-bold price-text">{{ order.total.toFixed(2) }} грн</td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>
          <div class="card-footer">
            <router-link to="/orders" class="btn btn-outline-primary">
              <i class="bi bi-arrow-left me-1"></i>Повернутися до списку замовлень
            </router-link>
          </div>
        </div>
      </div>
      
      <div class="col-lg-4">
        <!-- Статус заказа -->
        <div class="card mb-4">
          <div class="card-header bg-dark text-white">
            <h5 class="mb-0">Статус замовлення</h5>
          </div>
          <div class="card-body p-0">
            <ul class="list-group list-group-flush">
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <i class="bi bi-check-circle-fill text-success me-2"></i>
                  <span>Замовлення створено</span>
                </div>
                <span class="text-muted small">{{ formatDate(order.created_at) }}</span>
              </li>
              <li :class="['list-group-item', 'd-flex', 'justify-content-between', 'align-items-center', {'text-muted': order.status === 'CREATED'}]">
                <div>
                  <i :class="['bi', 'me-2', order.status === 'CREATED' ? 'bi-circle' : 'bi-check-circle-fill', order.status !== 'CREATED' ? 'text-success' : '']"></i>
                  <span>Оплата підтверджена</span>
                </div>
                <span v-if="order.status !== 'CREATED'" class="text-muted small">{{ formatDate(order.created_at) }}</span>
              </li>
              <li :class="['list-group-item', 'd-flex', 'justify-content-between', 'align-items-center', {'text-muted': !['ON_WAY', 'DELIVERED'].includes(order.status)}]">
                <div>
                  <i :class="['bi', 'me-2', !['ON_WAY', 'DELIVERED'].includes(order.status) ? 'bi-circle' : 'bi-check-circle-fill', ['ON_WAY', 'DELIVERED'].includes(order.status) ? 'text-success' : '']"></i>
                  <span>Відправлено</span>
                </div>
                <span v-if="['ON_WAY', 'DELIVERED'].includes(order.status)" class="text-muted small">{{ formatDate(order.created_at) }}</span>
              </li>
              <li :class="['list-group-item', 'd-flex', 'justify-content-between', 'align-items-center', {'text-muted': order.status !== 'DELIVERED'}]">
                <div>
                  <i :class="['bi', 'me-2', order.status !== 'DELIVERED' ? 'bi-circle' : 'bi-check-circle-fill', order.status === 'DELIVERED' ? 'text-success' : '']"></i>
                  <span>Доставлено</span>
                </div>
                <span v-if="order.status === 'DELIVERED'" class="text-muted small">{{ formatDate(order.created_at) }}</span>
              </li>
            </ul>
          </div>
        </div>
        
        <!-- Контактная информация -->
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Потрібна допомога?</h5>
          </div>
          <div class="card-body">
            <p>Якщо у вас виникли питання щодо вашого замовлення, будь ласка, зв'яжіться з нами:</p>
            <p class="mb-2">
              <i class="bi bi-telephone me-2"></i>+380 67 123 4567
            </p>
            <p class="mb-0">
              <i class="bi bi-envelope me-2"></i>orders@fixstar.com.ua
            </p>
            <hr>
            <p class="mb-0 small text-muted">При зверненні, будь ласка, вкажіть номер замовлення: {{ order.id }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.order-detail-view {
  padding-bottom: 30px;
}

.price-text {
  color: #ff6b00;
}
</style> 