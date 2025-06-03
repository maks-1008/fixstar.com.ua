<script>
import { useUserStore } from '@/stores'
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'ProfileView',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    
    const user = computed(() => userStore.user)
    const isEditing = ref(false)
    const isUpdating = ref(false)
    const isChangingPassword = ref(false)
    const updateSuccess = ref(false)
    const passwordUpdateSuccess = ref(false)
    const error = ref(null)
    
    const form = ref({
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      phone: '',
      address: '',
      city: ''
    })
    
    const passwordForm = ref({
      current_password: '',
      new_password: '',
      confirm_password: ''
    })
    
    onMounted(async () => {
      if (userStore.isAuthenticated) {
        await userStore.fetchUserData()
        
        // Заполняем форму данными пользователя
        form.value = {
          username: user.value.username,
          email: user.value.email,
          first_name: user.value.first_name,
          last_name: user.value.last_name,
          phone: user.value.phone,
          address: user.value.address || '',
          city: user.value.city || ''
        }
      }
    })
    
    const toggleEdit = () => {
      if (isEditing.value) {
        // Сбрасываем форму к исходным данным
        form.value = {
          username: user.value.username,
          email: user.value.email,
          first_name: user.value.first_name,
          last_name: user.value.last_name,
          phone: user.value.phone,
          address: user.value.address || '',
          city: user.value.city || ''
        }
      }
      
      isEditing.value = !isEditing.value
    }
    
    const updateProfile = async () => {
      try {
        isUpdating.value = true
        error.value = null
        
        await userStore.updateProfile({
          email: form.value.email,
          first_name: form.value.first_name,
          last_name: form.value.last_name,
          phone: form.value.phone,
          address: form.value.address,
          city: form.value.city
        })
        
        isEditing.value = false
        updateSuccess.value = true
        
        // Скрываем сообщение об успехе через 3 секунды
        setTimeout(() => {
          updateSuccess.value = false
        }, 3000)
      } catch (err) {
        error.value = err.message || 'Помилка оновлення профілю'
      } finally {
        isUpdating.value = false
      }
    }
    
    const changePassword = async () => {
      if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
        error.value = 'Паролі не співпадають'
        return
      }
      
      try {
        isChangingPassword.value = true
        error.value = null
        
        await userStore.changePassword({
          current_password: passwordForm.value.current_password,
          new_password: passwordForm.value.new_password
        })
        
        // Очищаем форму
        passwordForm.value = {
          current_password: '',
          new_password: '',
          confirm_password: ''
        }
        
        passwordUpdateSuccess.value = true
        
        // Скрываем сообщение об успехе через 3 секунды
        setTimeout(() => {
          passwordUpdateSuccess.value = false
        }, 3000)
      } catch (err) {
        error.value = err.message || 'Помилка зміни паролю'
      } finally {
        isChangingPassword.value = false
      }
    }
    
    const logout = async () => {
      await userStore.logout()
      router.push('/login')
    }
    
    return {
      user,
      isEditing,
      isUpdating,
      isChangingPassword,
      updateSuccess,
      passwordUpdateSuccess,
      error,
      form,
      passwordForm,
      toggleEdit,
      updateProfile,
      changePassword,
      logout
    }
  }
}
</script>

<template>
  <div class="profile-view">
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Завантаження...</span>
      </div>
    </div>
    
    <div v-else-if="!isAuthenticated" class="text-center py-5">
      <div class="alert alert-warning" role="alert">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        Увійдіть у свій обліковий запис, щоб переглянути профіль
      </div>
      <router-link to="/login" class="btn btn-primary">
        Увійти
      </router-link>
    </div>
    
    <div v-else class="row">
      <!-- Боковое меню -->
      <div class="col-lg-3 mb-4">
        <div class="card">
          <div class="card-header bg-dark text-white">
            <h5 class="mb-0">Меню користувача</h5>
          </div>
          <div class="list-group list-group-flush">
            <router-link to="/profile" class="list-group-item list-group-item-action active">
              <i class="bi bi-person-fill me-2"></i>Профіль
            </router-link>
            <router-link to="/orders" class="list-group-item list-group-item-action">
              <i class="bi bi-bag-fill me-2"></i>Мої замовлення
            </router-link>
            <a href="#" class="list-group-item list-group-item-action" @click.prevent="logout">
              <i class="bi bi-box-arrow-right me-2"></i>Вийти
            </a>
          </div>
        </div>
      </div>
      
      <!-- Профиль пользователя -->
      <div class="col-lg-9">
        <div class="card mb-4">
          <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Інформація профілю</h5>
            <button class="btn btn-sm btn-light" @click="toggleEdit">
              <i class="bi me-1" :class="isEditing ? 'bi-x-lg' : 'bi-pencil-fill'"></i>
              {{ isEditing ? 'Скасувати' : 'Редагувати' }}
            </button>
          </div>
          <div class="card-body">
            <form @submit.prevent="updateProfile" v-if="isEditing">
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="username" class="form-label">Логін</label>
                  <input type="text" class="form-control" id="username" v-model="form.username" disabled>
                </div>
                <div class="col-md-6">
                  <label for="email" class="form-label">Email</label>
                  <input type="email" class="form-control" id="email" v-model="form.email" required>
                </div>
              </div>
              
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="first_name" class="form-label">Ім'я</label>
                  <input type="text" class="form-control" id="first_name" v-model="form.first_name" required>
                </div>
                <div class="col-md-6">
                  <label for="last_name" class="form-label">Прізвище</label>
                  <input type="text" class="form-control" id="last_name" v-model="form.last_name" required>
                </div>
              </div>
              
              <div class="mb-3">
                <label for="phone" class="form-label">Телефон</label>
                <input type="tel" class="form-control" id="phone" v-model="form.phone" required>
              </div>
              
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="address" class="form-label">Адреса</label>
                  <input type="text" class="form-control" id="address" v-model="form.address">
                </div>
                <div class="col-md-6">
                  <label for="city" class="form-label">Місто</label>
                  <input type="text" class="form-control" id="city" v-model="form.city">
                </div>
              </div>
              
              <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-secondary me-2" @click="toggleEdit">Скасувати</button>
                <button type="submit" class="btn btn-primary" :disabled="isUpdating">
                  <span v-if="isUpdating" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Зберегти зміни
                </button>
              </div>
            </form>
            
            <div v-else>
              <div class="row mb-3">
                <div class="col-md-6">
                  <p class="mb-1 text-muted">Логін:</p>
                  <p class="fs-5">{{ user.username }}</p>
                </div>
                <div class="col-md-6">
                  <p class="mb-1 text-muted">Email:</p>
                  <p class="fs-5">{{ user.email }}</p>
                </div>
              </div>
              
              <div class="row mb-3">
                <div class="col-md-6">
                  <p class="mb-1 text-muted">Ім'я:</p>
                  <p class="fs-5">{{ user.first_name }}</p>
                </div>
                <div class="col-md-6">
                  <p class="mb-1 text-muted">Прізвище:</p>
                  <p class="fs-5">{{ user.last_name }}</p>
                </div>
              </div>
              
              <div class="mb-3">
                <p class="mb-1 text-muted">Телефон:</p>
                <p class="fs-5">{{ user.phone }}</p>
              </div>
              
              <div class="row mb-3">
                <div class="col-md-6">
                  <p class="mb-1 text-muted">Адреса:</p>
                  <p class="fs-5">{{ user.address || 'Не вказано' }}</p>
                </div>
                <div class="col-md-6">
                  <p class="mb-1 text-muted">Місто:</p>
                  <p class="fs-5">{{ user.city || 'Не вказано' }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="card">
          <div class="card-header bg-dark text-white">
            <h5 class="mb-0">Зміна паролю</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="changePassword">
              <div class="mb-3">
                <label for="current_password" class="form-label">Поточний пароль</label>
                <input type="password" class="form-control" id="current_password" v-model="passwordForm.current_password" required>
              </div>
              
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="new_password" class="form-label">Новий пароль</label>
                  <input type="password" class="form-control" id="new_password" v-model="passwordForm.new_password" required>
                </div>
                <div class="col-md-6">
                  <label for="confirm_password" class="form-label">Підтвердження паролю</label>
                  <input type="password" class="form-control" id="confirm_password" v-model="passwordForm.confirm_password" required>
                </div>
              </div>
              
              <div class="d-flex justify-content-end">
                <button type="submit" class="btn btn-primary" :disabled="isChangingPassword">
                  <span v-if="isChangingPassword" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Змінити пароль
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-view {
  padding-bottom: 30px;
}
</style> 