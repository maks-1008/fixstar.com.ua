<template>
  <div class="not-found-view">
    <div class="text-center py-5">
      <div class="error-code mb-4">404</div>
      <h1 class="mb-4">Сторінку не знайдено</h1>
      <p class="lead mb-5">Сторінка, яку ви шукаєте, не існує або була переміщена.</p>
      
      <div class="d-flex justify-content-center gap-3">
        <router-link to="/" class="btn btn-primary">
          <i class="bi bi-house-fill me-2"></i>На головну
        </router-link>
        <router-link to="/catalog" class="btn btn-outline-primary">
          <i class="bi bi-shop me-2"></i>До каталогу
        </router-link>
      </div>
    </div>
    
    <div class="row mt-5">
      <div class="col-md-6 offset-md-3">
        <div class="card">
          <div class="card-header bg-dark text-white">
            <h5 class="mb-0">Можливо, вас зацікавить</h5>
          </div>
          <div class="card-body">
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                <router-link to="/catalog" class="text-decoration-none">Каталог товарів</router-link>
              </li>
              <li class="list-group-item">
                <router-link to="/contacts" class="text-decoration-none">Контактна інформація</router-link>
              </li>
              <li class="list-group-item">
                <router-link to="/profile" class="text-decoration-none">Особистий кабінет</router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found-view {
  padding: 50px 0;
}

.error-code {
  font-size: 8rem;
  font-weight: 700;
  color: #dc3545;
  text-shadow: 4px 4px 0px rgba(0, 0, 0, 0.1);
  line-height: 1;
}
</style> 