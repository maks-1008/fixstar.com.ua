<script>
import { useProductStore } from '@/stores'
import { useCartStore } from '@/stores'
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'SubcategoryView',
  setup() {
    const productStore = useProductStore()
    const cartStore = useCartStore()
    const route = useRoute()
    const router = useRouter()
    
    const loading = ref(true)
    const subcategorySlug = computed(() => route.params.slug)
    
    // Фильтры
    const filters = ref({
      strength: '',
      coating: '',
      diameter: '',
      length: ''
    })
    
    const subcategory = computed(() => {
      return productStore.getSubcategoryBySlug(subcategorySlug.value)
    })
    
    const parentCategory = computed(() => {
      if (!subcategory.value) return null
      return productStore.categories.find(c => c.id === subcategory.value.category)
    })
    
    const products = computed(() => {
      if (!subcategory.value) return []
      return productStore.products.filter(p => p.subcategory === subcategory.value.id)
    })
    
    const filteredProducts = computed(() => {
      return products.value.filter(p => {
        return (!filters.value.strength || p.strength_class === filters.value.strength)
          && (!filters.value.coating || p.coating === filters.value.coating)
          && (!filters.value.diameter || p.diameters?.includes(filters.value.diameter))
          && (!filters.value.length || p.lengths?.includes(filters.value.length))
      })
    })
    
    // Уникальные значения для фильтров
    const uniqueStrengths = computed(() => {
      return [...new Set(products.value.map(p => p.strength_class).filter(Boolean))]
    })
    
    const uniqueCoatings = computed(() => {
      return [...new Set(products.value.map(p => p.coating).filter(Boolean))]
    })
    
    const uniqueDiameters = computed(() => {
      const allDiameters = products.value
        .map(p => p.diameters ? p.diameters.split(',').map(d => d.trim()) : [])
        .flat()
        .filter(Boolean)
      return [...new Set(allDiameters)]
    })
    
    const uniqueLengths = computed(() => {
      const allLengths = products.value
        .map(p => p.lengths ? p.lengths.split(',').map(l => l.trim()) : [])
        .flat()
        .filter(Boolean)
      return [...new Set(allLengths)]
    })
    
    // Добавление в корзину
    const addToCart = (product) => {
      cartStore.addToCart(product)
      alert(`Товар "${product.name}" додано до кошика!`)
    }
    
    onMounted(async () => {
      if (productStore.categories.length === 0) {
        await productStore.fetchCategories()
      }
      
      if (productStore.subcategories.length === 0) {
        await productStore.fetchSubcategories()
      }
      
      if (productStore.products.length === 0) {
        await productStore.fetchProducts()
      }
      
      loading.value = false
      
      // Если подкатегория не найдена, переходим на 404
      if (!loading.value && !subcategory.value) {
        router.push({ name: 'notFound' })
      }
    })
    
    const resetFilters = () => {
      filters.value = {
        strength: '',
        coating: '',
        diameter: '',
        length: ''
      }
    }
    
    return {
      subcategory,
      parentCategory,
      products,
      filteredProducts,
      loading,
      filters,
      uniqueStrengths,
      uniqueCoatings,
      uniqueDiameters,
      uniqueLengths,
      addToCart,
      resetFilters
    }
  }
}
</script>

<template>
  <div class="subcategory-view">
    <!-- Загрузка -->
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Завантаження...</span>
      </div>
      <p class="mt-2">Завантаження товарів...</p>
    </div>
    
    <!-- Содержимое подкатегории -->
    <div v-else-if="subcategory">
      <div class="subcategory-header mb-4">
        <h1>{{ subcategory.name }}</h1>
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb">
            <li class="breadcrumb-item"><router-link to="/">Головна</router-link></li>
            <li class="breadcrumb-item"><router-link to="/catalog">Каталог</router-link></li>
            <li class="breadcrumb-item" v-if="parentCategory">
              <router-link :to="{ name: 'category', params: { slug: parentCategory.slug }}">
                {{ parentCategory.name }}
              </router-link>
            </li>
            <li class="breadcrumb-item active" aria-current="page">{{ subcategory.name }}</li>
          </ol>
        </nav>
      </div>
      
      <!-- Изображение подкатегории -->
      <div v-if="subcategory.image" class="subcategory-image-container mb-4">
        <img :src="subcategory.image" :alt="subcategory.name" class="img-fluid subcategory-image">
      </div>
      
      <!-- Фильтры -->
      <div class="card mb-4" id="filter-section">
        <div class="card-header bg-dark text-white">
          <h5 class="mb-0">Фільтри товарів</h5>
        </div>
        <div class="card-body">
          <div class="row mb-3">
            <div class="col-md-3 mb-2" v-if="uniqueStrengths.length > 0">
              <label class="form-label">Клас міцності</label>
              <select v-model="filters.strength" class="form-select">
                <option value="">Всі</option>
                <option v-for="strength in uniqueStrengths" :key="strength" :value="strength">
                  {{ strength }}
                </option>
              </select>
            </div>
            <div class="col-md-3 mb-2" v-if="uniqueCoatings.length > 0">
              <label class="form-label">Покриття</label>
              <select v-model="filters.coating" class="form-select">
                <option value="">Всі</option>
                <option v-for="coating in uniqueCoatings" :key="coating" :value="coating">
                  {{ coating }}
                </option>
              </select>
            </div>
            <div class="col-md-3 mb-2" v-if="uniqueDiameters.length > 0">
              <label class="form-label">Діаметр, мм</label>
              <select v-model="filters.diameter" class="form-select">
                <option value="">Всі</option>
                <option v-for="diameter in uniqueDiameters" :key="diameter" :value="diameter">
                  {{ diameter }}
                </option>
              </select>
            </div>
            <div class="col-md-3 mb-2" v-if="uniqueLengths.length > 0">
              <label class="form-label">Довжина, мм</label>
              <select v-model="filters.length" class="form-select">
                <option value="">Всі</option>
                <option v-for="length in uniqueLengths" :key="length" :value="length">
                  {{ length }}
                </option>
              </select>
            </div>
          </div>
          <div class="text-end">
            <button @click="resetFilters" class="btn btn-outline-secondary">
              <i class="bi bi-x-circle me-1"></i> Скинути фільтри
            </button>
          </div>
        </div>
      </div>
      
      <!-- Список товаров -->
      <h2 class="mb-3">Товари ({{ filteredProducts.length }})</h2>
      <div v-if="filteredProducts.length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        <div v-for="product in filteredProducts" :key="product.id" class="col">
          <div class="card h-100 product-card">
            <div class="product-img-container">
              <i v-if="!product.image" class="bi bi-box product-icon"></i>
              <img v-else :src="product.image" class="card-img-top" :alt="product.name">
            </div>
            <div class="card-body">
              <h5 class="card-title">{{ product.name }}</h5>
              <p class="card-text text-muted small mb-1">Код: {{ product.code }}</p>
              <div class="product-specs small mb-2" v-if="product.strength_class || product.coating || product.diameters || product.lengths">
                <p class="mb-0" v-if="product.strength_class">
                  <strong>Клас міцності:</strong> {{ product.strength_class }}
                </p>
                <p class="mb-0" v-if="product.coating">
                  <strong>Покриття:</strong> {{ product.coating }}
                </p>
                <p class="mb-0" v-if="product.diameters">
                  <strong>Діаметр:</strong> {{ product.diameters }} мм
                </p>
                <p class="mb-0" v-if="product.lengths">
                  <strong>Довжина:</strong> {{ product.lengths }} мм
                </p>
              </div>
              <p class="card-text price-text fw-bold">{{ product.price }} грн</p>
            </div>
            <div class="card-footer d-flex justify-content-between">
              <router-link 
                :to="{ name: 'product', params: { slug: product.slug }}" 
                class="btn btn-sm btn-outline-primary"
              >
                <i class="bi bi-info-circle me-1"></i> Деталі
              </router-link>
              <button 
                @click="addToCart(product)" 
                class="btn btn-sm btn-primary"
              >
                <i class="bi bi-cart-plus me-1"></i> В кошик
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Пусто -->
      <div v-else class="text-center my-5">
        <i class="bi bi-exclamation-circle display-1 text-muted"></i>
        <h3 class="mt-3">Товарів не знайдено</h3>
        <p class="text-muted">Спробуйте змінити параметри фільтрації.</p>
        <button @click="resetFilters" class="btn btn-primary mt-2">
          <i class="bi bi-x-circle me-1"></i> Скинути фільтри
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.subcategory-view {
  padding-bottom: 30px;
}

.subcategory-image-container {
  max-height: 250px;
  overflow: hidden;
  border-radius: 8px;
}

.subcategory-image {
  width: 100%;
  height: 250px;
  object-fit: cover;
}

.product-card {
  transition: transform 0.3s;
  border: 1px solid #dee2e6;
  overflow: hidden;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.product-img-container {
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  overflow: hidden;
  padding: 10px;
}

.product-icon {
  font-size: 3.5rem;
  color: #6c757d;
}

.card-img-top {
  object-fit: contain;
  max-height: 100%;
  max-width: 100%;
}

.price-text {
  color: #ff6b00;
  font-size: 1.2rem;
}

.product-specs {
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
  padding: 5px 0;
}
</style> 