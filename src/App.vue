<script>
import { defineComponent } from 'vue'
import TheNavbar from '@/components/TheNavbar.vue'
import Sidebar from '@/components/Sidebar.vue'

export default defineComponent({
  name: 'App',
  components: {
    TheNavbar,
    Sidebar
  }
})
</script>

<template>
  <div class="app-container">
    <TheNavbar />
    <Sidebar />
    <router-view />
  </div>
</template>

<style>
/* Импорт Bootstrap Icons */
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css");

.app-container {
  width: 100%;
  min-height: 100vh;
  position: relative;
}

/* Добавляем отступ для контента чтобы он не перекрывался навигационной панелью */
.router-view-container {
  padding-top: 56px; /* Высота навигационной панели */
  margin-left: 180px; /* Отступ для сайдбара */
}

/* Глобальные стили */
body {
  margin: 0;
  padding: 0;
  font-family: 'Roboto', sans-serif;
}

/* Для правильной работы подменю в Sidebar */
.dropdown-menu {
  position: absolute;
}

/* Стили для карточек с тенями */
.card-shadow {
  box-shadow: 0 0 25px 5px rgba(0, 0, 0, 0.4), 0 0 50px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  background-color: white;
}
</style>