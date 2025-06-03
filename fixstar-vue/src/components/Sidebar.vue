<template>
  <div class="sidebar">
    <div class="category-menu">
      <!-- Кріплення -->
      <div class="dropdown-wrapper">
        <button class="category-btn main-category" @click="toggleMenu('fasteners')">
          <i class="bi bi-grid-3x3-gap-fill"></i> Кріплення
        </button>
        <div class="dropdown-menu" :class="{ 'show': activeMenu === 'fasteners' }">
          <!-- Анкери -->
          <div class="dropdown-submenu">
            <button class="dropdown-item" @mouseover="toggleSubmenu('anchors')">
              Анкери <i class="bi bi-chevron-right"></i>
            </button>
            <div class="submenu" :class="{ 'show': activeSubmenu === 'anchors' }">
              <router-link to="/category/anker-molly" class="dropdown-item" @click="closeAllMenus">Анкер MOLLY</router-link>
              <router-link to="/category/anker-bierbah" class="dropdown-item" @click="closeAllMenus">Анкер BIERBAH</router-link>
              <router-link to="/category/anker-etkd" class="dropdown-item" @click="closeAllMenus">Анкер ETKD</router-link>
              <router-link to="/category/anker-redibolt" class="dropdown-item" @click="closeAllMenus">Анкер REDIBOLT</router-link>
              <router-link to="/category/anker-tfc" class="dropdown-item" @click="closeAllMenus">Анкер TFC</router-link>
              <router-link to="/category/anker-tgs" class="dropdown-item" @click="closeAllMenus">Анкер TGS</router-link>
              <router-link to="/category/gvint-turbo" class="dropdown-item" @click="closeAllMenus">Гвинт TURBO</router-link>
              <router-link to="/category/dyubel-eto" class="dropdown-item" @click="closeAllMenus">Дюбель ETO</router-link>
              <router-link to="/category/himichni-ankeri-ta-aksesuari" class="dropdown-item" @click="closeAllMenus">Хімічні анкери та аксесуари</router-link>
              <router-link to="/category/anker-ethd" class="dropdown-item" @click="closeAllMenus">Анкер ETHD</router-link>
              <router-link to="/category/anker-dvorozpirnij-slr" class="dropdown-item" @click="closeAllMenus">Анкер дворозпірний SLR</router-link>
            </div>
          </div>
          
          <!-- Болти -->
          <div class="dropdown-submenu">
            <button class="dropdown-item" @mouseover="toggleSubmenu('bolts')">
              Болти <i class="bi bi-chevron-right"></i>
            </button>
            <div class="submenu" :class="{ 'show': activeSubmenu === 'bolts' }">
              <router-link to="/category/bolti-z-shestigrannoyu-golovkoyu" class="dropdown-item" @click="closeAllMenus">Болти з шестигранною головкою</router-link>
              <router-link to="/category/bolti-z-kvadratnim-pidgolovkom" class="dropdown-item" @click="closeAllMenus">Болти з квадратним підголовком</router-link>
              <router-link to="/category/bolti-z-kilcem" class="dropdown-item" @click="closeAllMenus">Болти з кільцем</router-link>
              <router-link to="/category/bolti-spec" class="dropdown-item" @click="closeAllMenus">Болти спец</router-link>
            </div>
          </div>
          
          <!-- Гайки -->
          <div class="dropdown-submenu">
            <button class="dropdown-item" @mouseover="toggleSubmenu('nuts')">
              Гайки <i class="bi bi-chevron-right"></i>
            </button>
            <div class="submenu" :class="{ 'show': activeSubmenu === 'nuts' }">
              <router-link to="/category/gajki-shestigranni" class="dropdown-item" @click="closeAllMenus">Гайки шестигранні</router-link>
              <router-link to="/category/gajki-krugli" class="dropdown-item" @click="closeAllMenus">Гайки круглі</router-link>
              <router-link to="/category/gajki-samostoporni" class="dropdown-item" @click="closeAllMenus">Гайки самостопорні</router-link>
              <router-link to="/category/gajki-rim-gajka" class="dropdown-item" @click="closeAllMenus">Рим-гайка</router-link>
              <router-link to="/category/gajka-z-flancem" class="dropdown-item" @click="closeAllMenus">Гайка з фланцем</router-link>
              <router-link to="/category/gajka-koronchata" class="dropdown-item" @click="closeAllMenus">Гайка корончата</router-link>
              <router-link to="/category/gajka-kovpachkova" class="dropdown-item" @click="closeAllMenus">Гайка ковпачкова</router-link>
              <router-link to="/category/gajka-baranceva" class="dropdown-item" @click="closeAllMenus">Гайка баранцева</router-link>
              <router-link to="/category/gajka-spec" class="dropdown-item" @click="closeAllMenus">Гайка спец</router-link>
            </div>
          </div>
          
          <!-- Гвинти -->
          <div class="dropdown-submenu">
            <button class="dropdown-item" @mouseover="toggleSubmenu('screws')">
              Гвинти <i class="bi bi-chevron-right"></i>
            </button>
            <div class="submenu" :class="{ 'show': activeSubmenu === 'screws' }">
              <router-link to="/category/gvinti-z-napivkrugloyu-golovkoyu" class="dropdown-item" @click="closeAllMenus">Гвинти з напівкруглою головкою</router-link>
              <router-link to="/category/gvinti-z-potajnoyu-golovkoyu" class="dropdown-item" @click="closeAllMenus">Гвинти з потайною головкою</router-link>
              <router-link to="/category/gvinti-z-cilindrichnoyu-golovkoyu" class="dropdown-item" @click="closeAllMenus">Гвинти з циліндричною головкою</router-link>
              <router-link to="/category/gvinti-ustanovochni" class="dropdown-item" @click="closeAllMenus">Гвинти установочні</router-link>
              <router-link to="/category/gvint-barancevij" class="dropdown-item" @click="closeAllMenus">Гвинт баранцевий</router-link>
              <router-link to="/category/gvint-z-kilcem" class="dropdown-item" @click="closeAllMenus">Гвинт з кільцем</router-link>
            </div>
          </div>

          <!-- Дюбелі -->
          <div class="dropdown-submenu">
            <button class="dropdown-item" @mouseover="toggleSubmenu('dowels')">
              Дюбелі <i class="bi bi-chevron-right"></i>
            </button>
            <div class="submenu" :class="{ 'show': activeSubmenu === 'dowels' }">
              <router-link to="/category/dyubeli-dlya-lgk" class="dropdown-item" @click="closeAllMenus">Дюбелі для ЛГК</router-link>
              <router-link to="/category/dyubeli-ramni" class="dropdown-item" @click="closeAllMenus">Дюбелі рамні</router-link>
              <router-link to="/category/dyubeli-universalni" class="dropdown-item" @click="closeAllMenus">Дюбелі універсальні</router-link>
              <router-link to="/category/dyubel-shvidkij-montazh" class="dropdown-item" @click="closeAllMenus">Дюбель швидкий монтаж</router-link>
              <router-link to="/category/termodyubel" class="dropdown-item" @click="closeAllMenus">Термодюбель</router-link>
              <router-link to="/category/dyubeli-dlya-gazobetona" class="dropdown-item" @click="closeAllMenus">Дюбелі для газобетона</router-link>
            </div>
          </div>

          <!-- Добавьте остальные подкатегории по аналогии -->
        </div>
      </div>
      
      <!-- Фарби -->
      <div class="dropdown-wrapper">
        <button class="category-btn" @click="toggleMenu('paints')">
          <i class="bi bi-paint-bucket"></i> Фарби
        </button>
        <div class="dropdown-menu" :class="{ 'show': activeMenu === 'paints' }">
          <!-- Первый уровень подкатегорий красок -->
          <div class="dropdown-submenu">
            <button class="dropdown-item" @mouseover="toggleSubmenu('paint-type-1')">
              Фасадні фарби <i class="bi bi-chevron-right"></i>
            </button>
            <div class="submenu" :class="{ 'show': activeSubmenu === 'paint-type-1' }">
              <router-link to="/category/farby-fasadni-1" class="dropdown-item" @click="closeAllMenus">Акрилові фасадні</router-link>
              <router-link to="/category/farby-fasadni-2" class="dropdown-item" @click="closeAllMenus">Силіконові фасадні</router-link>
            </div>
          </div>
          
          <div class="dropdown-submenu">
            <button class="dropdown-item" @mouseover="toggleSubmenu('paint-type-2')">
              Інтер'єрні фарби <i class="bi bi-chevron-right"></i>
            </button>
            <div class="submenu" :class="{ 'show': activeSubmenu === 'paint-type-2' }">
              <router-link to="/category/farby-interierni-1" class="dropdown-item" @click="closeAllMenus">Для стін</router-link>
              <router-link to="/category/farby-interierni-2" class="dropdown-item" @click="closeAllMenus">Для стелі</router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Інструмент -->
      <div class="dropdown-wrapper">
        <button class="category-btn" @click="toggleMenu('tools')">
          <i class="bi bi-tools"></i> Інструмент
        </button>
        <div class="dropdown-menu" :class="{ 'show': activeMenu === 'tools' }">
          <!-- Первый уровень подкатегорий инструментов -->
          <div class="dropdown-submenu">
            <button class="dropdown-item" @mouseover="toggleSubmenu('hand-tools')">
              Ручний інструмент <i class="bi bi-chevron-right"></i>
            </button>
            <div class="submenu" :class="{ 'show': activeSubmenu === 'hand-tools' }">
              <router-link to="/category/instrument-ruchnoi-1" class="dropdown-item" @click="closeAllMenus">Викрутки</router-link>
              <router-link to="/category/instrument-ruchnoi-2" class="dropdown-item" @click="closeAllMenus">Молотки</router-link>
              <router-link to="/category/instrument-ruchnoi-3" class="dropdown-item" @click="closeAllMenus">Пасатижі</router-link>
            </div>
          </div>
          
          <div class="dropdown-submenu">
            <button class="dropdown-item" @mouseover="toggleSubmenu('power-tools')">
              Електроінструмент <i class="bi bi-chevron-right"></i>
            </button>
            <div class="submenu" :class="{ 'show': activeSubmenu === 'power-tools' }">
              <router-link to="/category/instrument-electro-1" class="dropdown-item" @click="closeAllMenus">Дрилі</router-link>
              <router-link to="/category/instrument-electro-2" class="dropdown-item" @click="closeAllMenus">Перфоратори</router-link>
              <router-link to="/category/instrument-electro-3" class="dropdown-item" @click="closeAllMenus">Шуруповерти</router-link>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Корзина -->
      <router-link to="/cart" class="category-btn cart-btn">
        <i class="bi bi-cart"></i> {{ cartCount }}
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useCartStore } from '@/stores'

export default {
  name: 'Sidebar',
  setup() {
    const cartStore = useCartStore()
    const activeMenu = ref(null)
    const activeSubmenu = ref(null)
    
    // Вычисляемое свойство для количества товаров в корзине
    const cartCount = computed(() => {
      return cartStore.totalCount || 0
    })

    onMounted(() => {
      // Загрузка корзины при монтировании компонента
      cartStore.loadCart()
      
      // Добавление обработчика для закрытия меню при клике вне компонента
      document.addEventListener('click', handleOutsideClick)
    })
    
    // Удаление обработчика при уничтожении компонента
    onUnmounted(() => {
      document.removeEventListener('click', handleOutsideClick)
    })
    
    // Обработчик клика вне компонента
    const handleOutsideClick = (event) => {
      const sidebar = document.querySelector('.sidebar')
      if (sidebar && !sidebar.contains(event.target)) {
        closeAllMenus()
      }
    }
    
    // Методы управления меню
    const toggleMenu = (menu) => {
      if (activeMenu.value === menu) {
        activeMenu.value = null
        activeSubmenu.value = null
      } else {
        activeMenu.value = menu
        activeSubmenu.value = null
      }
    }
    
    const toggleSubmenu = (submenu) => {
      activeSubmenu.value = submenu
    }
    
    const closeAllMenus = () => {
      activeMenu.value = null
      activeSubmenu.value = null
    }
    
    return {
      activeMenu,
      activeSubmenu,
      cartCount,
      toggleMenu,
      toggleSubmenu,
      closeAllMenus
    }
  }
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 80px;
  top: 70px;
  z-index: 100;
  display: flex;
  flex-direction: column;
}

.category-menu {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.dropdown-wrapper {
  position: relative;
}

.category-btn {
  padding: 8px 15px;
  font-size: 16px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
  border-radius: 4px;
  background-color: rgba(33, 37, 41, 0.9);
  color: white;
  border: none;
  cursor: pointer;
  text-align: left;
  min-width: 140px;
  transition: all 0.2s ease;
  text-decoration: none;
}

.category-btn:hover {
  background-color: rgba(33, 37, 41, 1);
}

.category-btn i {
  font-size: 16px;
  width: 20px;
  display: flex;
  justify-content: center;
}

.dropdown-menu {
  position: absolute;
  left: 100%;
  top: 0;
  background-color: rgba(33, 37, 41, 0.95);
  border-radius: 4px;
  display: none;
  min-width: 200px;
  padding: 10px 0;
  z-index: 1000;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  margin-left: 5px;
}

.dropdown-menu.show {
  display: block;
}

.dropdown-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 15px;
  color: white;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
  width: 100%;
  background: none;
  border: none;
  text-align: left;
  font-size: 14px;
}

.dropdown-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffa023;
}

.dropdown-submenu {
  position: relative;
  width: 100%;
}

.submenu {
  position: absolute;
  left: 100%;
  top: 0;
  background-color: rgba(33, 37, 41, 0.95);
  border-radius: 4px;
  display: none;
  min-width: 280px;
  padding: 10px 0;
  z-index: 1001;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  margin-left: 5px;
}

.submenu.show {
  display: block;
}

.cart-btn {
  background-color: #ffa023;
}

.cart-btn:hover {
  background-color: #e89020;
}

@media (max-width: 768px) {
  .sidebar {
    position: static;
    width: 100%;
    height: auto;
    padding: 10px;
    margin-top: 60px;
  }

  .category-menu {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 10px;
    padding: 10px;
  }

  .dropdown-menu {
    position: fixed;
    left: 0;
    top: auto;
    width: 100%;
    max-height: 60vh;
    overflow-y: auto;
    margin-left: 0;
  }

  .submenu {
    position: fixed;
    left: 0;
    top: auto;
    width: 100%;
    max-height: 60vh;
    overflow-y: auto;
    margin-left: 0;
  }
}
</style> 