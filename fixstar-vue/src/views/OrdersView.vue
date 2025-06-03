<script>
import { useOrderStore } from '@/stores'
import { useUserStore } from '@/stores'
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'OrdersView',
  setup() {
    const orderStore = useOrderStore()
    const userStore = useUserStore()
    const router = useRouter()
    
    const orders = computed(() => orderStore.orders)
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
        router.push({ name: 'login', query: { redirect: '/orders' } })
        return
      }
      
      try {
        isLoading.value = true
        await orderStore.fetchOrders(userStore.user.id)
      } catch (err) {
        error.value = 'Помилка при завантаженні замовлень'
        console.error(err)
      } finally {
        isLoading.value = false
      }
    })
    
    return {
      orders,
      isLoading,
      error,
      formatDate,
      getStatusClass,
      getStatusText
    }
  }
}
</script>

<template>
  <div class="orders-view">
    <h1 class="mb-4">Мої замовлення</h1>
    
    <!-- Загрузка -->
    <div v-if="isLoading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Завантаження...</span>
      </div>
      <p class="mt-2">Завантаження замовлень...</p>
    </div>
    
    <!-- Ошибка -->
    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>
    
    <!-- Список заказов -->
    <div v-else>
      <div class="row">
        <div class="col-lg-8">
          <div v-if="orders.length > 0">
            <div class="card mb-4" v-for="order in orders" :key="order.id">
              <div class="card-header d-flex justify-content-between align-items-center">
                <div>
                  <span class="fs-5">Замовлення № {{ order.id }}</span>
                  <span class="ms-3 text-muted small">{{ formatDate(order.created_at) }}</span>
                </div>
                <span :class="['badge', getStatusClass(order.status)]">
                  {{ getStatusText(order.status) }}
                </span>
              </div>
              <div class="card-body">
                <div class="order-items mb-3">
                  <div v-for="item in order.items" :key="item.id" class="order-item mb-2">
                    <div class="d-flex justify-content-between">
                      <div>
                        <span class="item-name">{{ item.name }}</span>
                        <span class="text-muted small ms-2">{{ item.quantity }} x {{ item.price }} грн</span>
                      </div>
                      <div class="item-total">
                        {{ (item.quantity * item.price).toFixed(2) }} грн
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <span class="fs-5 fw-bold">Загальна сума:</span>
                  </div>
                  <div class="fs-5 fw-bold price-text">
                    {{ order.total.toFixed(2) }} грн
                  </div>
                </div>
              </div>
              <div class="card-footer d-flex justify-content-end">
                <router-link 
                  :to="{ name: 'order', params: { id: order.id }}" 
                  class="btn btn-outline-primary btn-sm"
                >
                  <i class="bi bi-eye me-1"></i>Деталі замовлення
                </router-link>
              </div>
            </div>
          </div>
          
          <!-- Пусто -->
          <div v-else class="text-center my-5">
            <i class="bi bi-bag-x display-1 text-muted"></i>
            <h3 class="mt-3">У вас поки немає замовлень</h3>
            <p class="text-muted mb-4">Перейдіть у каталог, щоб зробити перше замовлення.</p>
            <router-link to="/catalog" class="btn btn-primary">
              <i class="bi bi-shop me-2"></i>Перейти до каталогу
            </router-link>
          </div>
        </div>
        
        <div class="col-lg-4">
          <!-- Боковая панель -->
          <div class="card mb-4">
            <div class="card-header bg-dark text-white">
              <h5 class="mb-0">Навігація</h5>
            </div>
            <div class="card-body">
              <div class="list-group">
                <router-link to="/profile" class="list-group-item list-group-item-action">
                  <i class="bi bi-person me-2"></i>Мій профіль
                </router-link>
                <router-link to="/orders" class="list-group-item list-group-item-action active">
                  <i class="bi bi-bag me-2"></i>Мої замовлення
                </router-link>
              </div>
            </div>
          </div>
          
          <!-- Информационный блок -->
          <div class="card">
            <div class="card-header bg-info text-white">
              <h5 class="mb-0">Відстеження замовлень</h5>
            </div>
            <div class="card-body">
              <p>Ви можете відстежити статус вашого замовлення у розділі "Деталі замовлення".</p>
              <p class="mb-0">Якщо у вас виникли питання, будь ласка, зв'яжіться з нами за телефоном:</p>
              <p class="fw-bold mt-2">+380 67 123 4567</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.orders-view {
  padding-bottom: 30px;
}

.order-item {
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.order-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.item-name {
  font-weight: 500;
}

.price-text {
  color: #ff6b00;
}
</style> 