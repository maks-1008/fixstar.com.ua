import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CatalogView from '../views/CatalogView.vue'
import AboutView from '../views/AboutView.vue'
import DeliveryView from '../views/DeliveryView.vue'
import ContactsView from '../views/ContactsView.vue'
import CategoryView from '../views/CategoryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/catalog',
      name: 'catalog',
      component: CatalogView
    },
    {
      path: '/category/:slug',
      name: 'category',
      component: CategoryView
    },
    {
      path: '/subcategory/:slug',
      name: 'subcategory',
      component: () => import('../views/SubcategoryView.vue'),
    },
    {
      path: '/product/:slug',
      name: 'product',
      component: () => import('../views/ProductView.vue'),
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import('../views/CartView.vue'),
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: () => import('../views/CheckoutView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/orders',
      name: 'orders',
      component: () => import('../views/OrdersView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/order/:id',
      name: 'order',
      component: () => import('../views/OrderDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/delivery',
      name: 'delivery',
      component: DeliveryView
    },
    {
      path: '/contacts',
      name: 'contacts',
      component: ContactsView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path: '/info',
      name: 'info',
      component: () => import('../views/InfoView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'notFound',
      component: () => import('../views/NotFoundView.vue'),
    }
  ],
})

// Защита маршрутов
router.beforeEach((to, from, next) => {
  // Проверка на авторизацию через localStorage
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'
  
  // Если маршрут требует авторизации и пользователь не авторизован
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
