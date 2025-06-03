<script>
import { useUserStore } from '@/stores'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'RegisterView',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    
    const formData = ref({
      username: '',
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
      password: '',
      confirmPassword: ''
    })
    
    const isLoading = ref(false)
    const error = ref(null)
    
    const register = async () => {
      // Валидация формы
      if (!formData.value.username || !formData.value.password || !formData.value.confirmPassword) {
        error.value = 'Будь ласка, заповніть всі обов\'язкові поля'
        return
      }
      
      if (formData.value.password !== formData.value.confirmPassword) {
        error.value = 'Паролі не співпадають'
        return
      }
      
      isLoading.value = true
      error.value = null
      
      try {
        // Регистрация пользователя
        await userStore.register(formData.value)
        
        // Переход на страницу профиля
        router.push('/profile')
      } catch (err) {
        error.value = err.message || 'Помилка при реєстрації'
        console.error(err)
      } finally {
        isLoading.value = false
      }
    }
    
    return {
      formData,
      isLoading,
      error,
      register
    }
  }
}
</script>

<template>
  <div class="register-view">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <div class="card shadow">
          <div class="card-header bg-dark text-white">
            <h4 class="mb-0">Реєстрація</h4>
          </div>
          <div class="card-body p-4">
            <!-- Сообщение об ошибке -->
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            
            <form @submit.prevent="register">
              <div class="row g-3">
                <!-- Логин -->
                <div class="col-12">
                  <label for="username" class="form-label">Логін *</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="username" 
                    v-model="formData.username" 
                    required
                    autocomplete="username"
                  >
                  <div class="form-text">Мінімум 3 символи, тільки латинські літери та цифри</div>
                </div>
                
                <!-- Имя и фамилия -->
                <div class="col-md-6">
                  <label for="firstName" class="form-label">Ім'я</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="firstName" 
                    v-model="formData.firstName"
                  >
                </div>
                <div class="col-md-6">
                  <label for="lastName" class="form-label">Прізвище</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="lastName" 
                    v-model="formData.lastName"
                  >
                </div>
                
                <!-- Контактная информация -->
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
                  <label for="phone" class="form-label">Телефон</label>
                  <input 
                    type="tel" 
                    class="form-control" 
                    id="phone" 
                    v-model="formData.phone"
                  >
                </div>
                
                <!-- Пароли -->
                <div class="col-md-6">
                  <label for="password" class="form-label">Пароль *</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    id="password" 
                    v-model="formData.password" 
                    required
                    autocomplete="new-password"
                  >
                  <div class="form-text">Мінімум 6 символів</div>
                </div>
                <div class="col-md-6">
                  <label for="confirmPassword" class="form-label">Підтвердження паролю *</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    id="confirmPassword" 
                    v-model="formData.confirmPassword" 
                    required
                    autocomplete="new-password"
                  >
                </div>
                
                <div class="col-12 mt-4">
                  <div class="d-grid">
                    <button 
                      type="submit" 
                      class="btn btn-primary" 
                      :disabled="isLoading"
                    >
                      <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      <i v-else class="bi bi-person-plus me-2"></i>
                      Зареєструватися
                    </button>
                  </div>
                </div>
              </div>
            </form>
            
            <div class="mt-4 text-center">
              <p class="mb-0">Вже зареєстровані?</p>
              <router-link to="/login" class="text-decoration-none">
                Увійти в особистий кабінет
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-view {
  padding: 40px 0;
  max-width: 800px;
  margin: 0 auto;
}
</style> 