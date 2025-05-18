from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # path('login/', views.login, name='login'), # Старый путь входа
    # path('registration/', views.registration, name='registration'), # Старый путь регистрации
    path('signup/', views.login_signup_view, name='login_signup'), # Новый комбинированный путь
    path('profile/', views.profile, name='profile'),
    path('users-cart/', views.users_cart, name='users_cart'),
    path('logout/', views.logout, name='logout'),
]

