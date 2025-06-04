<template>
  <nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
    <div class="container">
      <router-link class="navbar-brand" to="/">Home</router-link>
      <button
        class="navbar-toggler"
        type="button"
        @click="toggleMobileMenu"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        class="collapse navbar-collapse"
        :class="{ show: mobileMenuOpen }"
        id="navbarSupportedContent"
      >
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item dropdown" :class="{ show: infoDropdownOpen }">
            <a
              class="nav-link dropdown-toggle text-white"
              href="#"
              role="button"
              @click.prevent="toggleInfoDropdown"
            >
              Інформація
            </a>
            <ul class="dropdown-menu" :class="{ show: infoDropdownOpen }">
              <li>
                <router-link
                  class="dropdown-item text-white"
                  to="/delivery"
                  @click="closeDropdowns"
                >
                  Доставка і оплата
                </router-link>
              </li>
              <li>
                <router-link
                  class="dropdown-item text-white"
                  to="/contacts"
                  @click="closeDropdowns"
                >
                  Контактна інформація
                </router-link>
              </li>
              <li>
                <router-link class="dropdown-item text-white" to="/about" @click="closeDropdowns">
                  Про нас
                </router-link>
              </li>
            </ul>
          </li>
          <li class="nav-item">
            <router-link class="nav-link text-white" to="/cart">Кошик</router-link>
          </li>
          <!-- Пример авторизации -->
          <li class="nav-item">
            <router-link class="nav-link text-white" to="/login">Вхід</router-link>
          </li>
        </ul>
        <form class="d-flex" @submit.prevent="searchProducts">
          <input
            class="form-control me-2"
            type="search"
            v-model="searchQuery"
            placeholder="Поиск товаров..."
            aria-label="Search"
          />
          <button class="btn btn-outline-success" type="submit">Пошук</button>
        </form>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'TheNavbar',
  data() {
    return {
      searchQuery: '',
      infoDropdownOpen: false,
      mobileMenuOpen: false,
    }
  },
  mounted() {
    // Добавляем обработчик для закрытия меню при клике вне его
    document.addEventListener('click', this.handleOutsideClick)
  },
  beforeUnmount() {
    // Удаляем обработчик при уничтожении компонента
    document.removeEventListener('click', this.handleOutsideClick)
  },
  methods: {
    toggleInfoDropdown() {
      this.infoDropdownOpen = !this.infoDropdownOpen
    },
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeDropdowns() {
      this.infoDropdownOpen = false
      this.mobileMenuOpen = false
    },
    handleOutsideClick(event) {
      // Закрываем выпадающее меню при клике вне его
      const dropdown = this.$el.querySelector('.dropdown')
      if (dropdown && !dropdown.contains(event.target)) {
        this.infoDropdownOpen = false
      }
    },
    searchProducts() {
      // Реализуем поиск товаров
      if (this.searchQuery.trim()) {
        this.$router.push({
          name: 'search',
          query: { q: this.searchQuery },
        })
        this.closeDropdowns()
      }
    },
  },
}
</script>

<style scoped>
.navbar {
  position: fixed;
  width: 100%;
  top: 0;
  z-index: 1000;
}

.dropdown-menu {
  display: none;
  background-color: #212529;
  position: absolute;
  min-width: 10rem;
  margin: 0;
}

.dropdown-menu.show {
  display: block;
}

.dropdown-item {
  color: white;
}

.dropdown-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffa023 !important;
}

/* Убираем стрелку у выпадающего меню */
.dropdown-toggle::after {
  display: none;
}

/* Медиа-запросы для мобильных устройств */
@media (max-width: 768px) {
  .navbar .container {
    padding: 0 10px;
  }

  .navbar-brand {
    font-size: 1.2rem;
  }

  .form-control {
    width: auto;
  }

  /* Стилизация выпадающего меню на мобильных */
  .navbar-collapse {
    background-color: rgba(33, 37, 41, 0.95);
    border-radius: 0 0 10px 10px;
    padding: 10px;
  }

  .dropdown-menu {
    position: static;
    float: none;
    width: 100%;
    margin-top: 5px;
    background-color: #1a1d20;
    border-radius: 5px;
  }

  .dropdown-item {
    padding: 8px 15px;
  }
}

/* Для очень маленьких экранов */
@media (max-width: 576px) {
  .navbar-brand {
    max-width: 120px;
    font-size: 1rem;
  }

  .form-control,
  .btn {
    font-size: 0.8rem;
    padding: 0.25rem 0.5rem;
  }

  .navbar-toggler {
    padding: 0.2rem 0.5rem;
    font-size: 1rem;
  }
}
</style>
