import { defineStore } from 'pinia'

// Хранилище для товаров
export const useProductStore = defineStore('products', {
  state: () => ({
    products: [],
    categories: [],
    subcategories: [],
    featuredProducts: [],
    loading: false,
    error: null
  }),
  getters: {
    getProductById: (state) => (id) => {
      return state.products.find(product => product.id === id)
    },
    getCategoryBySlug: (state) => (slug) => {
      return state.categories.find(category => category.slug === slug)
    },
    getSubcategoryBySlug: (state) => (slug) => {
      return state.subcategories.find(subcategory => subcategory.slug === slug)
    },
    getSubcategoriesByCategory: (state) => (categoryId) => {
      return state.subcategories.filter(subcategory => subcategory.category === categoryId)
    }
  },
  actions: {
    async fetchProducts() {
      this.loading = true
      try {
        // В реальном приложении это был бы API-запрос
        // const response = await fetch('/api/products')
        // const data = await response.json()
        
        // Временное решение с имитацией данных
        setTimeout(() => {
          this.products = [
            { id: 1, name: 'Гвинт самонарізний 5.8x70', price: 2.50, image: '/images/screw.jpg', slug: 'gvint-samonariznyj-5-8x70', subcategory: 1, code: 'SCR-001', description: 'Якісний гвинт самонарізний для будівельних робіт' },
            { id: 2, name: 'Фарба інтерєрна 5л', price: 320, image: '/images/paint.jpg', slug: 'farba-intererna-5l', subcategory: 2, code: 'PNT-001', description: 'Фарба для внутрішніх робіт' },
            { id: 3, name: 'Набір інструментів 56шт', price: 1200, image: '/images/toolset.jpg', slug: 'nabir-instrumentiv-56sht', subcategory: 3, code: 'TLS-001', description: 'Повний набір інструментів для домашнього майстра' }
          ]
          this.loading = false
        }, 500)
      } catch (error) {
        this.error = error.message
        this.loading = false
      }
    },
    async fetchCategories() {
      this.loading = true
      try {
        // В реальном приложении это был бы API-запрос
        setTimeout(() => {
          this.categories = [
            { id: 1, name: 'Кріплення', slug: 'fasteners', image: '/images/fasteners.jpg' },
            { id: 2, name: 'Фарби', slug: 'paints', image: '/images/paints.jpg' },
            { id: 3, name: 'Інструмент', slug: 'tools', image: '/images/tools.jpg' }
          ]
          this.loading = false
        }, 300)
      } catch (error) {
        this.error = error.message
        this.loading = false
      }
    },
    async fetchSubcategories() {
      this.loading = true
      try {
        // В реальном приложении это был бы API-запрос
        setTimeout(() => {
          this.subcategories = [
            { id: 1, name: 'Шурупи і саморізи', slug: 'screws', category: 1, image: '/images/screws.jpg' },
            { id: 2, name: 'Інтерєрні фарби', slug: 'interior-paints', category: 2, image: '/images/interior-paints.jpg' },
            { id: 3, name: 'Ручний інструмент', slug: 'hand-tools', category: 3, image: '/images/hand-tools.jpg' }
          ]
          this.loading = false
        }, 300)
      } catch (error) {
        this.error = error.message
        this.loading = false
      }
    },
    async fetchFeaturedProducts() {
      this.loading = true
      try {
        // В реальном приложении это был бы API-запрос
        setTimeout(() => {
          this.featuredProducts = [
            { id: 1, name: 'Гвинт самонарізний 5.8x70', price: 2.50, image: '/images/screw.jpg', slug: 'gvint-samonariznyj-5-8x70' },
            { id: 2, name: 'Фарба інтерєрна 5л', price: 320, image: '/images/paint.jpg', slug: 'farba-intererna-5l' },
            { id: 3, name: 'Набір інструментів 56шт', price: 1200, image: '/images/toolset.jpg', slug: 'nabir-instrumentiv-56sht' }
          ]
          this.loading = false
        }, 300)
      } catch (error) {
        this.error = error.message
        this.loading = false
      }
    }
  }
})

// Хранилище для корзины
export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    loading: false,
    error: null
  }),
  getters: {
    totalItems: (state) => {
      return state.items.reduce((total, item) => total + item.quantity, 0)
    },
    totalPrice: (state) => {
      return state.items.reduce((total, item) => total + (item.price * item.quantity), 0)
    }
  },
  actions: {
    addToCart(product, quantity = 1) {
      const existingItem = this.items.find(item => item.id === product.id)
      
      if (existingItem) {
        existingItem.quantity += quantity
      } else {
        this.items.push({
          id: product.id,
          name: product.name,
          price: product.price,
          image: product.image,
          quantity: quantity
        })
      }
      
      // Сохраняем корзину в localStorage
      localStorage.setItem('cart', JSON.stringify(this.items))
    },
    removeFromCart(productId) {
      const index = this.items.findIndex(item => item.id === productId)
      
      if (index !== -1) {
        this.items.splice(index, 1)
        localStorage.setItem('cart', JSON.stringify(this.items))
      }
    },
    updateQuantity(productId, quantity) {
      const item = this.items.find(item => item.id === productId)
      
      if (item) {
        item.quantity = quantity
        localStorage.setItem('cart', JSON.stringify(this.items))
      }
    },
    clearCart() {
      this.items = []
      localStorage.removeItem('cart')
    },
    loadCart() {
      const savedCart = localStorage.getItem('cart')
      
      if (savedCart) {
        this.items = JSON.parse(savedCart)
      }
    }
  }
})

// Хранилище для пользователя
export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null
  }),
  actions: {
    login(credentials) {
      this.loading = true
      
      // Имитация API-запроса
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          if (credentials.username === 'admin' && credentials.password === 'admin') {
            const user = {
              id: 1,
              username: 'admin',
              firstName: 'Админ',
              lastName: 'Админович',
              email: 'admin@example.com',
              phone: '+380671234567'
            }
            
            this.user = user
            this.isAuthenticated = true
            localStorage.setItem('user', JSON.stringify(user))
            localStorage.setItem('isAuthenticated', 'true')
            
            this.loading = false
            resolve(user)
          } else {
            this.error = 'Неправильний логін або пароль'
            this.loading = false
            reject(new Error('Неправильний логін або пароль'))
          }
        }, 800)
      })
    },
    logout() {
      this.user = null
      this.isAuthenticated = false
      localStorage.removeItem('user')
      localStorage.removeItem('isAuthenticated')
    },
    register(userData) {
      this.loading = true
      
      // Имитация API-запроса
      return new Promise((resolve) => {
        setTimeout(() => {
          const user = {
            id: Date.now(),
            username: userData.username,
            firstName: userData.firstName,
            lastName: userData.lastName,
            email: userData.email,
            phone: userData.phone
          }
          
          this.user = user
          this.isAuthenticated = true
          localStorage.setItem('user', JSON.stringify(user))
          localStorage.setItem('isAuthenticated', 'true')
          
          this.loading = false
          resolve(user)
        }, 800)
      })
    },
    checkAuth() {
      const savedUser = localStorage.getItem('user')
      const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'
      
      if (savedUser && isAuthenticated) {
        this.user = JSON.parse(savedUser)
        this.isAuthenticated = true
      }
    }
  }
})

// Хранилище для заказов
export const useOrderStore = defineStore('orders', {
  state: () => ({
    orders: [],
    loading: false,
    error: null
  }),
  getters: {
    getOrderById: (state) => (id) => {
      return state.orders.find(order => order.id === id)
    }
  },
  actions: {
    async fetchOrders(userId) {
      this.loading = true
      
      // Имитация API-запроса
      return new Promise((resolve) => {
        setTimeout(() => {
          // Генерируем несколько тестовых заказов
          this.orders = [
            { 
              id: '1.250523', 
              items: [
                { id: 1, name: 'Гвинт самонарізний 5.8x70', price: 2.50, quantity: 10 }
              ],
              total: 25.00,
              status: 'DELIVERED',
              created_at: '2023-05-25T14:30:00'
            },
            { 
              id: '2.260523', 
              items: [
                { id: 2, name: 'Фарба інтерєрна 5л', price: 320, quantity: 1 }
              ],
              total: 320.00,
              status: 'PAID',
              created_at: '2023-05-26T10:15:00'
            }
          ]
          
          this.loading = false
          resolve(this.orders)
        }, 800)
      })
    },
    async createOrder(orderData) {
      this.loading = true
      
      // Имитация API-запроса
      return new Promise((resolve) => {
        setTimeout(() => {
          const newOrder = {
            id: `${this.orders.length + 1}.${new Date().toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: '2-digit' }).replace(/\./g, '')}`,
            items: orderData.items,
            total: orderData.total,
            status: 'CREATED',
            created_at: new Date().toISOString()
          }
          
          this.orders.push(newOrder)
          this.loading = false
          resolve(newOrder)
        }, 800)
      })
    }
  }
}) 