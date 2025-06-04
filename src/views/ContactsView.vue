<template>
  <div class="contacts-view">
    <div class="background-container"></div>

    <div class="content-overlay">
      <div class="contacts-card">
        <h1>Контактна інформація</h1>

        <div class="contacts-section">
          <div class="contact-item">
            <img src="/images/location.png" alt="Адреса" />
            <a href="https://surl.li/dtqmyl" target="_blank">
              Адреса: вул. Чумацький Шлях, 72, Полтава, Україна, 36000
            </a>
          </div>

          <div class="contact-item">
            <img src="/images/Lifecell.png" alt="Lifecell" />
            <span>063-447-48-46</span>
          </div>

          <div class="contact-item">
            <img src="/images/Vodafone.png" alt="Vodafone" />
            <span>099-708-69-84</span>
          </div>

          <div class="contact-item">
            <img src="/images/email.png" alt="Email" />
            <a href="mailto:office@fixstar.com.ua">office@fixstar.com.ua</a>
          </div>
        </div>

        <div class="cta-section">
          <p>Зв'яжіться з нами сьогодні!</p>
        </div>
      </div>

      <!-- Копирайт внизу -->
      <footer class="copyright">© FixStar 2024 Всі права захищені</footer>
    </div>
  </div>
</template>

<style scoped>
.contacts-view {
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

.contacts-card {
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

h1 {
  color: #333;
  font-weight: 700;
  font-size: 2.2rem;
  margin-bottom: 30px;
  margin-top: 0;
}

.contacts-section {
  margin-bottom: 30px;
}

.contact-item {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.contact-item:last-child {
  margin-bottom: 0;
}

.contact-item img {
  width: 24px;
  height: 24px;
  margin-right: 15px;
}

.contact-item a,
.contact-item span {
  font-size: 1.1rem;
  color: #333;
  text-decoration: none;
  line-height: 1.5;
}

.contact-item a:hover {
  color: #ffa023;
}

.cta-section {
  margin-top: 30px;
}

.cta-section p {
  font-size: 1.2rem;
  color: #333;
  margin: 0;
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

  .contacts-card {
    position: relative;
    top: auto;
    left: auto;
    transform: none;
    margin: 80px auto 60px;
    width: 95%;
    padding: 20px;
  }

  .copyright {
    position: fixed;
  }
}
</style>
