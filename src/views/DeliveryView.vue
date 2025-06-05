<template>
  <div class="delivery-view">
    <div class="background-container"></div>

    <div class="content-overlay">
      <div class="delivery-card">
        <h1>Доставка і оплата</h1>

        <div class="delivery-section">
          <h3>Доставка:</h3>
          <ul>
            <li>
              по Україні кур'єрами транспортних компаній. Доставку товару оплачує покупець згідно з
              тарифами перевізника;
            </li>
            <li>
              в Полтаві та Полтавській області можлива безкоштовна доставка власним транспортом
              компанії при сумі замовлення від 5000 грн;
            </li>
            <li>
              самовивіз зі складу в Полтаві, вул. Чумацький Шлях, 72, графік роботи складу
              9:00-16:00 щодня.
            </li>
          </ul>
        </div>

        <div class="delivery-section">
          <h3>Способи оплати:</h3>
          <ul>
            <li>накладений платіж;</li>
            <li>оплата на сайті платіжною картою;</li>
            <li>безготівковий розрахунок;</li>
            <li>відстрочка платежу згідно з індивідуальним договором (для постійних клієнтів).</li>
          </ul>
        </div>

        <div class="delivery-section">
          <p>
            Відвантаження товару замовнику відбувається в день оплати або наступного робочого дня,
            якщо оплата надійшла після 14:00. Умови оплати та доставки узгоджуються під час
            остаточного оформлення замовлення.
          </p>
        </div>
      </div>

      <!-- Копирайт внизу -->
      <footer class="copyright">© FixStar 2024 Всі права захищені</footer>
    </div>
  </div>
</template>

<style scoped>
.delivery-view {
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

.delivery-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 5px 5px 25px 19px rgba(0, 0, 0, 0.5);
  padding: 30px 40px;
  max-width: 900px;
  width: 90%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  max-height: none;
  overflow-y: visible;
  animation: cardAppear 0.5s ease-out;
}

@keyframes cardAppear {
  from {
    opacity: 0;
    transform: translate(-50%, -48%);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
}

h1 {
  color: #333;
  font-weight: 700;
  font-size: 2.2rem;
  margin-bottom: 25px;
  margin-top: 0;
}

.delivery-section {
  margin-bottom: 20px;
}

h3 {
  color: #333;
  margin-top: 0;
  margin-bottom: 12px;
  font-weight: 700;
  font-size: 1.5rem;
}

ul {
  padding-left: 25px;
  margin-top: 0;
  margin-bottom: 0;
}

li {
  margin-bottom: 6px;
  line-height: 1.4;
  font-size: 1rem;
}

li:last-child {
  margin-bottom: 0;
}

p {
  margin: 0;
  line-height: 1.5;
  font-size: 1rem;
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

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .background-container {
    background-image: url('/images/bg-image5.jpg');
  }

  .delivery-view {
    position: absolute;
    height: auto;
    min-height: 100vh;
    overflow-y: auto;
  }

  .delivery-card {
    position: relative;
    top: auto;
    left: auto;
    transform: none;
    margin: 80px auto 60px;
    width: 85%;
    padding: 20px;
    max-height: none;
    overflow-y: visible;
  }

  .content-overlay {
    overflow-y: auto;
    height: auto;
    min-height: 100vh;
  }

  .copyright {
    position: fixed;
  }
}

/* Добавим стили для body через глобальные стили */
:global(body) {
  overflow-x: hidden;
  margin: 0;
  padding: 0;
}
</style>
