<script setup>
import { onMounted } from 'vue'
import { useProductStore } from '@/stores'

const productStore = useProductStore()

// Загружаем данные при монтировании компонента
onMounted(async () => {
  await productStore.fetchCategories()
})
</script>

<template>
  <div class="home-view">
    <div class="background-container"></div>
    
    <div class="content-overlay">
      <!-- Телефоны справа вверху -->
      <div class="phones-container">
        <div class="phone-item">
          <img src="/images/Lifecell.png" alt="Lifecell" class="operator-icon" />
          <a href="tel:063-447-48-46" class="phone-number">063-447-48-46</a>
        </div>

        <div class="phone-item">
          <img src="/images/Vodafone.png" alt="Vodafone" class="operator-icon" />
          <a href="tel:099-708-69-84" class="phone-number">099-708-69-84</a>
        </div>
      </div>

      <!-- Копирайт внизу -->
      <footer class="copyright">
        © FixStar 2024 Всі права захищені
      </footer>
    </div>
  </div>
</template>

<style scoped>
.home-view {
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
  background-image: url('/images/bg-image.jpg');
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

/* Телефоны */
.phones-container {
  position: absolute;
  top: 80px;
  right: 50px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.phone-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.operator-icon {
  width: 44px;
  height: 44px;
  object-fit: contain;
}

.phone-number {
  color: #003366;
  font-size: 44px;
  font-weight: 700;
  text-decoration: none;
  letter-spacing: 0.5px;
}

.phone-number:hover {
  color: #e89020;
  text-decoration: none;
}

/* Копирайт */
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
  .phones-container {
    position: static;
    margin: 20px;
    align-items: center;
  }
  
  .phone-number {
    font-size: 30px;
  }

  .copyright {
    position: fixed;
  }
}
</style>
