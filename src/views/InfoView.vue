<template>
  <div class="info-view">
    <h1 class="mb-4">Про компанію</h1>

    <div class="row">
      <div class="col-lg-8">
        <!-- О компании -->
        <div class="card mb-4">
          <div class="card-header bg-dark text-white">
            <h5 class="mb-0">Наша історія</h5>
          </div>
          <div class="card-body">
            <div class="mb-4">
              <p>
                <strong>FixStar</strong> – це інтернет-магазин метизів, фарб та ручного інструменту,
                який працює на ринку України з 2015 року. За цей час ми здобули довіру багатьох
                клієнтів та зарекомендували себе як надійний постачальник якісної продукції.
              </p>
              <p>
                Наша компанія була заснована групою ентузіастів, які мали досвід роботи в
                будівельній галузі та розуміли потреби професіоналів і домашніх майстрів. Ми почали
                з невеликого асортименту кріпильних виробів, але з часом розширили каталог до
                декількох тисяч найменувань товарів.
              </p>
              <p>
                Сьогодні <strong>FixStar</strong> – це сучасний інтернет-магазин з широким
                асортиментом товарів для будівництва, ремонту та господарства. Ми працюємо напряму з
                виробниками та офіційними дистриб'юторами, що дозволяє нам пропонувати якісну
                продукцію за доступними цінами.
              </p>
            </div>

            <div class="row mb-4">
              <div class="col-md-6 mb-3 mb-md-0">
                <img src="@/assets/about-1.jpg" alt="Наш магазин" class="img-fluid rounded" />
              </div>
              <div class="col-md-6">
                <img src="@/assets/about-2.jpg" alt="Наша команда" class="img-fluid rounded" />
              </div>
            </div>

            <blockquote class="blockquote text-center my-4">
              <p class="mb-0">
                "Наша мета – забезпечити кожного клієнта якісними товарами за доступними цінами та
                надати професійну консультацію з будь-якого питання."
              </p>
              <footer class="blockquote-footer mt-2">
                Директор компанії <cite title="Source Title">Олександр Петренко</cite>
              </footer>
            </blockquote>
          </div>
        </div>

        <!-- Наши преимущества -->
        <div class="card mb-4">
          <div class="card-header bg-dark text-white">
            <h5 class="mb-0">Наші переваги</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-4">
                <div class="advantage-item">
                  <div class="advantage-icon">
                    <i class="bi bi-award text-primary"></i>
                  </div>
                  <h5>Якісні товари</h5>
                  <p>Ми пропонуємо лише сертифіковану продукцію від перевірених виробників.</p>
                </div>
              </div>

              <div class="col-md-6 mb-4">
                <div class="advantage-item">
                  <div class="advantage-icon">
                    <i class="bi bi-currency-exchange text-primary"></i>
                  </div>
                  <h5>Доступні ціни</h5>
                  <p>Завдяки прямим поставкам від виробників ми тримаємо конкурентні ціни.</p>
                </div>
              </div>

              <div class="col-md-6 mb-4">
                <div class="advantage-item">
                  <div class="advantage-icon">
                    <i class="bi bi-truck text-primary"></i>
                  </div>
                  <h5>Швидка доставка</h5>
                  <p>Відправляємо замовлення в день оформлення при оформленні до 15:00.</p>
                </div>
              </div>

              <div class="col-md-6 mb-4">
                <div class="advantage-item">
                  <div class="advantage-icon">
                    <i class="bi bi-people text-primary"></i>
                  </div>
                  <h5>Професійні консультації</h5>
                  <p>Наші спеціалісти завжди готові допомогти з вибором товару.</p>
                </div>
              </div>

              <div class="col-md-6 mb-4">
                <div class="advantage-item">
                  <div class="advantage-icon">
                    <i class="bi bi-box-seam text-primary"></i>
                  </div>
                  <h5>Широкий асортимент</h5>
                  <p>Більше 5000 найменувань товарів для будівництва та ремонту.</p>
                </div>
              </div>

              <div class="col-md-6 mb-4">
                <div class="advantage-item">
                  <div class="advantage-icon">
                    <i class="bi bi-shield-check text-primary"></i>
                  </div>
                  <h5>Гарантія та повернення</h5>
                  <p>Гарантія на всі товари та можливість повернення протягом 14 днів.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Наши клиенты -->
        <div class="card">
          <div class="card-header bg-dark text-white">
            <h5 class="mb-0">Наші клієнти</h5>
          </div>
          <div class="card-body">
            <p>
              Ми працюємо як з фізичними особами, так і з будівельними компаніями, майстернями,
              виробництвами та магазинами. Серед наших клієнтів:
            </p>

            <div class="row">
              <div class="col-md-3 col-6 mb-4 text-center">
                <img src="@/assets/client-1.png" alt="Клієнт 1" class="img-fluid client-logo" />
              </div>
              <div class="col-md-3 col-6 mb-4 text-center">
                <img src="@/assets/client-2.png" alt="Клієнт 2" class="img-fluid client-logo" />
              </div>
              <div class="col-md-3 col-6 mb-4 text-center">
                <img src="@/assets/client-3.png" alt="Клієнт 3" class="img-fluid client-logo" />
              </div>
              <div class="col-md-3 col-6 mb-4 text-center">
                <img src="@/assets/client-4.png" alt="Клієнт 4" class="img-fluid client-logo" />
              </div>
            </div>

            <div class="text-center mt-3">
              <p>Приєднуйтесь до наших задоволених клієнтів вже сьогодні!</p>
              <router-link to="/catalog" class="btn btn-primary">
                <i class="bi bi-shop me-2"></i>Перейти до каталогу
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Боковая панель -->
      <div class="col-lg-4">
        <!-- Контакты -->
        <div class="card mb-4">
          <div class="card-header bg-dark text-white">
            <h5 class="mb-0">Контактна інформація</h5>
          </div>
          <div class="card-body">
            <div class="d-flex align-items-start mb-3">
              <i class="bi bi-geo-alt-fill text-primary fs-4 me-3"></i>
              <div>
                <h6>Адреса:</h6>
                <p class="mb-0">вул. Примакова, 46, м. Київ, 04074</p>
              </div>
            </div>

            <div class="d-flex align-items-start mb-3">
              <i class="bi bi-telephone-fill text-primary fs-4 me-3"></i>
              <div>
                <h6>Телефони:</h6>
                <p class="mb-1">+380 67 123 4567</p>
                <p class="mb-0">+380 50 987 6543</p>
              </div>
            </div>

            <div class="d-flex align-items-start mb-3">
              <i class="bi bi-envelope-fill text-primary fs-4 me-3"></i>
              <div>
                <h6>Email:</h6>
                <p class="mb-0">info@fixstar.com.ua</p>
              </div>
            </div>

            <div class="d-flex align-items-start">
              <i class="bi bi-clock-fill text-primary fs-4 me-3"></i>
              <div>
                <h6>Графік роботи:</h6>
                <p class="mb-1">Пн-Пт: 9:00 - 18:00</p>
                <p class="mb-0">Сб: 9:00 - 15:00, Нд: вихідний</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Вакансии -->
        <div class="card mb-4">
          <div class="card-header bg-dark text-white">
            <h5 class="mb-0">Вакансії</h5>
          </div>
          <div class="card-body">
            <p>
              Ми постійно розвиваємося та шукаємо нових талановитих співробітників до нашої команди.
            </p>
            <div class="list-group">
              <a href="#" class="list-group-item list-group-item-action">
                <div class="d-flex w-100 justify-content-between">
                  <h6 class="mb-1">Менеджер з продажу</h6>
                  <small class="text-muted">Повна зайнятість</small>
                </div>
              </a>
              <a href="#" class="list-group-item list-group-item-action">
                <div class="d-flex w-100 justify-content-between">
                  <h6 class="mb-1">Комірник</h6>
                  <small class="text-muted">Повна зайнятість</small>
                </div>
              </a>
              <a href="#" class="list-group-item list-group-item-action">
                <div class="d-flex w-100 justify-content-between">
                  <h6 class="mb-1">Водій-експедитор</h6>
                  <small class="text-muted">Повна зайнятість</small>
                </div>
              </a>
            </div>
            <div class="mt-3">
              <p>
                Для отримання детальної інформації про вакансії, будь ласка, надсилайте резюме на
                email: <a href="mailto:hr@fixstar.com.ua">hr@fixstar.com.ua</a>
              </p>
            </div>
          </div>
        </div>

        <!-- Соцсети -->
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Ми в соціальних мережах</h5>
          </div>
          <div class="card-body">
            <p>
              Підписуйтесь на наші сторінки в соціальних мережах, щоб бути в курсі новин та акцій:
            </p>
            <div class="d-flex justify-content-around social-icons">
              <a href="#" class="text-decoration-none">
                <i class="bi bi-facebook fs-2 text-primary"></i>
              </a>
              <a href="#" class="text-decoration-none">
                <i class="bi bi-instagram fs-2 text-danger"></i>
              </a>
              <a href="#" class="text-decoration-none">
                <i class="bi bi-telegram fs-2 text-info"></i>
              </a>
              <a href="#" class="text-decoration-none">
                <i class="bi bi-youtube fs-2 text-danger"></i>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.info-view {
  padding-bottom: 30px;
}

.advantage-item {
  padding: 15px;
  border-radius: 5px;
  height: 100%;
  transition: all 0.3s ease;
}

.advantage-item:hover {
  background-color: #f8f9fa;
  transform: translateY(-5px);
}

.advantage-icon {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.client-logo {
  max-height: 80px;
  filter: grayscale(100%);
  transition: all 0.3s ease;
}

.client-logo:hover {
  filter: grayscale(0%);
}

.social-icons a {
  transition: all 0.3s ease;
}

.social-icons a:hover {
  transform: scale(1.2);
}
</style>
