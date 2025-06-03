<script>
import { useProductStore } from '@/stores'
import { useCartStore } from '@/stores'
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'ProductView',
  setup() {
    const productStore = useProductStore()
    const cartStore = useCartStore()
    const route = useRoute()
    const router = useRouter()
    
    const loading = ref(true)
    const productSlug = computed(() => route.params.slug)
    const quantity = ref(1)
    
    const product = computed(() => {
      return productStore.products.find(p => p.slug === productSlug.value)
    })
    
    const subcategory = computed(() => {
      if (!product.value) return null
      return productStore.getSubcategoryBySlug(product.value.subcategory)
    })
    
    const category = computed(() => {
      if (!subcategory.value) return null
      return productStore.getCategoryBySlug(subcategory.value.category)
    })
    
    const addToCart = () => {
      cartStore.addToCart(product.value, quantity.value)
      alert(`${quantity.value} од. товару "${product.value.name}" додано до кошика!`)
    }
    
    const increaseQuantity = () => {
      quantity.value++
    }
    
    const decreaseQuantity = () => {
      if (quantity.value > 1) {
        quantity.value--
      }
    }
    
    onMounted(async () => {
      if (productStore.products.length === 0) {
        await productStore.fetchProducts()
      }
      
      if (productStore.subcategories.length === 0) {
        await productStore.fetchSubcategories()
      }
      
      if (productStore.categories.length === 0) {
        await productStore.fetchCategories()
      }
      
      loading.value = false
      
      // Если товар не найден, переходим на 404
      if (!loading.value && !product.value) {
        router.push({ name: 'notFound' })
      }
    })
    
    return {
      product,
      subcategory,
      category,
      loading,
      quantity,
      addToCart,
      increaseQuantity,
      decreaseQuantity
    }
  }
}
</script>

<template>
  <div class="product-view">
    <!-- Загрузка -->
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Завантаження...</span>
      </div>
      <p class="mt-2">Завантаження товару...</p>
    </div>
    
    <!-- Содержимое товара -->
    <div v-else-if="product">
      <!-- Хлебные крошки -->
      <nav aria-label="breadcrumb" class="mb-4">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><router-link to="/">Головна</router-link></li>
          <li class="breadcrumb-item"><router-link to="/catalog">Каталог</router-link></li>
          <li class="breadcrumb-item" v-if="category">
            <router-link :to="{ name: 'category', params: { slug: category.slug }}">
              {{ category.name }}
            </router-link>
          </li>
          <li class="breadcrumb-item" v-if="subcategory">
            <router-link :to="{ name: 'subcategory', params: { slug: subcategory.slug }}">
              {{ subcategory.name }}
            </router-link>
          </li>
          <li class="breadcrumb-item active" aria-current="page">{{ product.name }}</li>
        </ol>
      </nav>
      
      <div class="row">
        <!-- Изображение товара -->
        <div class="col-lg-5 mb-4">
          <div class="product-image-container">
            <i v-if="!product.image" class="bi bi-box-seam product-placeholder-icon"></i>
            <img v-else :src="product.image" :alt="product.name" class="img-fluid product-image">
          </div>
        </div>
        
        <!-- Информация о товаре -->
        <div class="col-lg-7">
          <h1 class="product-title mb-2">{{ product.name }}</h1>
          <p class="text-muted mb-3">Код товару: {{ product.code }}</p>
          
          <!-- Характеристики -->
          <div class="product-specs mb-4" v-if="product.strength_class || product.coating || product.diameters || product.lengths">
            <h5>Характеристики:</h5>
            <div class="table-responsive">
              <table class="table table-striped">
                <tbody>
                  <tr v-if="product.strength_class">
                    <th scope="row">Клас міцності</th>
                    <td>{{ product.strength_class }}</td>
                  </tr>
                  <tr v-if="product.coating">
                    <th scope="row">Покриття</th>
                    <td>{{ product.coating }}</td>
                  </tr>
                  <tr v-if="product.diameters">
                    <th scope="row">Діаметр, мм</th>
                    <td>{{ product.diameters }}</td>
                  </tr>
                  <tr v-if="product.lengths">
                    <th scope="row">Довжина, мм</th>
                    <td>{{ product.lengths }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <!-- Цена и добавление в корзину -->
          <div class="product-price-section p-4 rounded mb-4">
            <div class="row align-items-center">
              <div class="col-md-6">
                <h3 class="price-text mb-0">{{ product.price }} грн</h3>
                <p v-if="product.quantity > 0" class="text-success mb-0 mt-2">
                  <i class="bi bi-check-circle"></i> В наявності
                </p>
                <p v-else class="text-danger mb-0 mt-2">
                  <i class="bi bi-x-circle"></i> Немає в наявності
                </p>
              </div>
              <div class="col-md-6">
                <div class="input-group mb-3">
                  <button class="btn btn-outline-secondary" type="button" @click="decreaseQuantity">-</button>
                  <input type="number" class="form-control text-center" v-model="quantity" min="1">
                  <button class="btn btn-outline-secondary" type="button" @click="increaseQuantity">+</button>
                </div>
                <button 
                  @click="addToCart" 
                  class="btn btn-primary w-100"
                  :disabled="product.quantity <= 0"
                >
                  <i class="bi bi-cart-plus me-2"></i> Додати в кошик
                </button>
              </div>
            </div>
          </div>
          
          <!-- Описание товара -->
          <div v-if="product.description" class="product-description mb-4">
            <h5>Опис:</h5>
            <p>{{ product.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.product-view {
  padding-bottom: 30px;
}

.product-image-container {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
  min-height: 300px;
  padding: 20px;
}

.product-placeholder-icon {
  font-size: 6rem;
  color: #6c757d;
}

.product-image {
  object-fit: contain;
  max-height: 400px;
  max-width: 100%;
}

.product-title {
  font-weight: 600;
  color: #212529;
}

.product-price-section {
  background-color: #f8f9fa;
  border-left: 5px solid #ff6b00;
}

.price-text {
  color: #ff6b00;
  font-weight: 600;
}

.product-specs table {
  font-size: 0.95rem;
}

.product-specs th {
  width: 40%;
}
</style> 