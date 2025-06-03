<template>
  <div class="catalog">
    <h1 class="mb-4">Каталог товарів</h1>
    
    <!-- Поиск по категориям -->
    <div class="search-container mb-4">
      <div class="input-group">
        <input 
          type="text" 
          class="form-control" 
          placeholder="Пошук категорій..." 
          v-model="searchQuery"
        >
        <button class="btn btn-outline-secondary" type="button">
          <i class="bi bi-search"></i>
        </button>
      </div>
    </div>

    <!-- Загрузка -->
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Завантаження...</span>
      </div>
      <p class="mt-2">Завантаження категорій...</p>
    </div>

    <!-- Список категорий -->
    <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div v-for="category in filteredCategories" :key="category.id" class="col">
        <div class="card h-100 category-card">
          <div class="category-img-container">
            <i v-if="!category.image" class="bi bi-box category-icon"></i>
            <img v-else :src="category.image" class="card-img-top" :alt="category.name">
          </div>
          <div class="card-body">
            <h5 class="card-title">{{ category.name }}</h5>
            <router-link 
              :to="{ name: 'category', params: { slug: category.slug }}" 
              class="btn btn-primary mt-2"
            >
              Переглянути
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Пусто -->
    <div v-if="!loading && filteredCategories.length === 0" class="text-center my-5">
      <i class="bi bi-exclamation-circle display-1 text-muted"></i>
      <h3 class="mt-3">Категорії не знайдено</h3>
      <p class="text-muted">Спробуйте змінити параметри пошуку.</p>
    </div>
  </div>
</template>

<script>
import { useProductStore } from '@/stores'
import { onMounted, ref, computed } from 'vue'

export default {
  name: 'CatalogView',
  setup() {
    const productStore = useProductStore()
    const loading = ref(true)
    const searchQuery = ref('')
    const selectedCategory = ref(null)

    const categories = computed(() => productStore.categories)
    const filteredCategories = computed(() => {
      if (!searchQuery.value) return categories.value
      return categories.value.filter(category => 
        category.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    onMounted(async () => {
      await productStore.fetchCategories()
      loading.value = false
    })

    return {
      categories,
      filteredCategories,
      loading,
      searchQuery,
      selectedCategory
    }
  }
}
</script>

<style scoped>
.catalog {
  padding-bottom: 30px;
}

.category-card {
  transition: transform 0.3s;
  border: 1px solid #dee2e6;
  overflow: hidden;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.category-img-container {
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  overflow: hidden;
}

.category-icon {
  font-size: 4rem;
  color: #6c757d;
}

.card-img-top {
  object-fit: cover;
  height: 100%;
  width: 100%;
}

.search-container {
  max-width: 500px;
  margin: 0 auto;
}
</style> 