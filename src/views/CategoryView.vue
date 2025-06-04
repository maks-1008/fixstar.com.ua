<script>
import { useProductStore } from '@/stores'
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'

export default {
  name: 'CategoryView',
  components: {
    Sidebar,
  },
  setup() {
    const productStore = useProductStore()
    const route = useRoute()
    const router = useRouter()

    const loading = ref(true)
    const categorySlug = computed(() => route.params.slug)

    const category = computed(() => {
      return productStore.getCategoryBySlug(categorySlug.value)
    })

    const subcategories = computed(() => {
      if (!category.value) return []
      return productStore.getSubcategoriesByCategory(category.value.id)
    })

    const products = ref([])
    const categoryTitle = ref('Болти з шестигранною головкою')
    const categoryDescription = ref(
      'Болти з шестигранною головкою застосовуються для створення нерозємних зєднань. Вони мають шестигранну головку та різьбу метричну.',
    )

    onMounted(async () => {
      if (productStore.categories.length === 0) {
        await productStore.fetchCategories()
      }

      if (productStore.subcategories.length === 0) {
        await productStore.fetchSubcategories()
      }

      loading.value = false

      // Если категория не найдена, переходим на 404
      if (!loading.value && !category.value) {
        router.push({ name: 'notFound' })
      }

      // Здесь будет запрос к API для получения товаров категории
      // Используем параметр маршрута для определения какую категорию загружать
      console.log('Loading category:', categorySlug.value)

      // Заглушка для демо-данных
      // В реальном приложении тут будет API запрос
      // this.fetchProducts(categorySlug.value)
    })

    const fetchProducts = () => {
      // Здесь будет запрос к API
      // В реальном приложении будет что-то типа:
      // axios.get(`/api/category/${categorySlug.value}/products`)
      //   .then(response => {
      //     products.value = response.data.products
      //     categoryTitle.value = response.data.title
      //     categoryDescription.value = response.data.description
      //   })
    }

    return {
      category,
      subcategories,
      loading,
      products,
      categoryTitle,
      categoryDescription,
      fetchProducts,
    }
  },
}
</script>

<template>
  <div class="category-view">
    <div class="background-container"></div>

    <div class="content-overlay">
      <!-- Импортируем боковое меню -->
      <Sidebar />

      <div class="category-content">
        <div class="category-header">
          <h1>{{ categoryTitle }}</h1>
          <div class="category-description">
            {{ categoryDescription }}
          </div>
        </div>

        <div class="product-grid">
          <!-- Здесь будет список товаров -->
          <div v-for="product in products" :key="product.id" class="product-card">
            <div class="product-image">
              <img :src="product.image" :alt="product.name" />
            </div>
            <div class="product-info">
              <h3>{{ product.name }}</h3>
              <div class="product-code">{{ product.code }}</div>
              <div class="product-price">{{ product.price }} грн</div>
              <button class="add-to-cart-btn"><i class="bi bi-cart-plus"></i> В корзину</button>
            </div>
          </div>

          <!-- Пример продуктов для демонстрации -->
          <div v-if="products.length === 0" class="product-card">
            <div class="product-image">
              <img src="/images/goods/DIN931.webp" alt="DIN 931" />
            </div>
            <div class="product-info">
              <h3>DIN 931</h3>
              <div class="product-code">Болт з шестигранною головкою</div>
              <div class="product-price">25.50 грн</div>
              <button class="add-to-cart-btn"><i class="bi bi-cart-plus"></i> В корзину</button>
            </div>
          </div>

          <div v-if="products.length === 0" class="product-card">
            <div class="product-image">
              <img src="/images/goods/DIN933.webp" alt="DIN 933" />
            </div>
            <div class="product-info">
              <h3>DIN 933</h3>
              <div class="product-code">Болт з шестигранною головкою</div>
              <div class="product-price">28.75 грн</div>
              <button class="add-to-cart-btn"><i class="bi bi-cart-plus"></i> В корзину</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Копирайт внизу -->
      <footer class="copyright">© FixStar 2024 Всі права захищені</footer>
    </div>
  </div>
</template>

<style scoped>
.category-view {
  position: fixed;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  margin: 0;
  padding: 0;
  top: 0;
  left: 0;
}

.background-container {
  position: fixed;
  width: 100%;
  height: 100%;
  background-image: url('/images/bg-image4.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
}

.content-overlay {
  position: relative;
  width: 100%;
  height: 100%;
  z-index: 1;
  overflow: hidden;
}

.category-content {
  background-color: white;
  border-radius: 8px;
  box-shadow: 5px 5px 25px 19px rgba(0, 0, 0, 0.5);
  padding: 30px;
  max-width: 1200px;
  width: 90%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  height: 80vh;
  overflow-y: auto;
}

.category-header {
  margin-bottom: 30px;
  border-bottom: 1px solid #eee;
  padding-bottom: 20px;
}

.category-header h1 {
  color: #333;
  font-size: 1.8rem;
  margin-bottom: 10px;
}

.category-description {
  color: #666;
  font-size: 1rem;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
}

.product-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition:
    transform 0.3s,
    box-shadow 0.3s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
}

.product-image {
  height: 180px;
  overflow: hidden;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.product-info {
  padding: 15px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.product-info h3 {
  font-size: 1.2rem;
  margin: 0 0 8px 0;
  color: #333;
}

.product-code {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 12px;
}

.product-price {
  font-size: 1.3rem;
  font-weight: bold;
  color: #222;
  margin-bottom: 15px;
  margin-top: auto;
}

.add-to-cart-btn {
  background-color: #ffa023;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background-color 0.2s;
  width: 100%;
}

.add-to-cart-btn:hover {
  background-color: #e89020;
}

.copyright {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  text-align: center;
  background-color: #212529;
  color: white;
  font-size: 16px;
  padding: 6px 0;
  margin: 0;
  line-height: 1.2;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

@media (max-width: 768px) {
  .background-container {
    background-image: url('/images/bg-image5.jpg');
  }

  .category-content {
    position: relative;
    top: auto;
    left: auto;
    transform: none;
    margin: 80px auto 60px;
    width: 95%;
    height: auto;
    max-height: none;
  }

  .product-grid {
    grid-template-columns: 1fr;
  }

  .copyright {
    position: fixed;
  }
}
</style>
