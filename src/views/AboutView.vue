<template>
  <div class="about-view">
    <div class="background-container"></div>

    <div class="content-overlay">
      <div class="about-card">
        <div class="company-name">
          <span class="fixstar">
            <span class="text-blue">Fix</span><span class="text-orange">Star</span>
          </span>
        </div>

        <div class="about-section">
          <p>
            FixStar - інтернет-магазин кріпильних матеріалів, фарби та інструментів. Наші товари
            стануть у пригоді всім, хто пов'язаний з будівництвом, ремонтом, монтажем обладнання та
            різних конструкцій. У нас обслуговуються як фізичні так і юридичні осіби. Підтримується
            готівкова та безготівкова оплата. На більшість товарів надаються постійні накопичувальні
            знижки, деякі товари знижки від обсягу купівлі. У разі оптових замовлень можливі
            спеціальні договірні умови.
          </p>
        </div>

        <div class="values-section">
          <h3>Головним для нас є:</h3>
          <ul>
            <li>якість наших товарів</li>
            <li>високий рівень обслуговування клієнтів</li>
            <li>довгострокова співпраця з партнерами</li>
            <li>розвиток власного бренду</li>
          </ul>
        </div>

        <div class="cta-section">
          <p>
            Якщо вам сподобався наш товар, натискайте на кнопку "Замовити" та оформлюйте заявку!
          </p>
        </div>
      </div>

      <!-- Копирайт внизу -->
      <footer class="copyright">© FixStar 2024 Всі права захищені</footer>
    </div>
  </div>
</template>

<style scoped>
.about-view {
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

.about-card {
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

.company-name {
  text-align: center;
  margin-bottom: 25px;
}

.fixstar {
  font-size: 2.5rem;
  font-weight: 900;
}

.text-blue {
  color: #083765;
  font-weight: 900;
}

.text-orange {
  color: #ffa023;
  font-weight: 900;
}

.about-section {
  margin-bottom: 30px;
}

.values-section {
  margin-bottom: 30px;
}

h3 {
  color: #333;
  margin-top: 0;
  margin-bottom: 15px;
  font-weight: 700;
  font-size: 1.5rem;
}

ul {
  padding-left: 25px;
  margin-top: 0;
  margin-bottom: 0;
}

li {
  margin-bottom: 8px;
  line-height: 1.5;
  font-size: 1rem;
}

p {
  margin: 0;
  line-height: 1.6;
  font-size: 1.1rem;
  color: #333;
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

  .about-view {
    position: absolute;
    height: auto;
    min-height: 100vh;
    overflow-y: auto;
  }

  .about-card {
    position: relative;
    top: auto;
    left: auto;
    transform: none;
    margin: 80px auto 60px;
    width: 85%;
    padding: 20px;
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
</style>
