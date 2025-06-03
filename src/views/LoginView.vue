<script>
import { useUserStore } from '@/stores'
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'LoginView',
  setup() {
    const userStore = useUserStore()
    const route = useRoute()
    const router = useRouter()
    
    const credentials = ref({
      username: '',
      password: ''
    })
    
    const isLoading = ref(false)
    const error = ref(null)
    
    const redirectPath = computed(() => route.query.redirect || '/')
    
    const login = async () => {
      // Валидация формы
      if (!credentials.value.username || !credentials.value.password) {
        error.value = 'Будь ласка, заповніть всі поля'
        return
      }
      
      isLoading.value = true
      error.value = null
      
      try {
        await userStore.login(credentials.value)
        
        // Переход на страницу перенаправления
        router.push(redirectPath.value)
      } catch (err) {
        error.value = err.message || 'Помилка при вході'
        console.error(err)
      } finally {
        isLoading.value = false
      }
    }
    
    return {
      credentials,
      isLoading,
      error,
      login
    }
  }
}
</script>

<template>
  <div class="login-view">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-5">
        <div class="card shadow">
          <div class="card-header bg-dark text-white">
            <h4 class="mb-0">Вхід в особистий кабінет</h4>
          </div>
          <div class="card-body p-4">
            <!-- Сообщение об ошибке -->
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            
            <form @submit.prevent="login">
              <div class="mb-3">
                <label for="username" class="form-label">Логін</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="username" 
                  v-model="credentials.username" 
                  required
                  autocomplete="username"
                >
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Пароль</label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="password" 
                  v-model="credentials.password" 
                  required
                  autocomplete="current-password"
                >
              </div>
              <div class="d-grid">
                <button 
                  type="submit" 
                  class="btn btn-primary" 
                  :disabled="isLoading"
                >
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  <i v-else class="bi bi-box-arrow-in-right me-2"></i>
                  Увійти
                </button>
              </div>
            </form>
            
            <div class="mt-4 text-center">
              <p class="mb-0">Ще не зареєстровані?</p>
              <router-link to="/register" class="text-decoration-none">
                Створити новий акаунт
              </router-link>
            </div>
          </div>
          <div class="card-footer text-center text-muted">
            <p class="mb-2">Для демонстрації використовуйте:</p>
            <p class="mb-0">Логін: <strong>admin</strong> / Пароль: <strong>admin</strong></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-view {
  padding: 40px 0;
  max-width: 600px;
  margin: 0 auto;
}
</style> 