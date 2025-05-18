from django.urls import path
from . import views

app_name = 'carts'  # Пространство имён приложения

urlpatterns = [
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('', views.cart_view, name='cart_view'),  # Главная страница корзины
    path('change/<int:product_id>/', views.cart_change, name='cart_change'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('session-change/', views.session_change, name='session_change'),
    path('session-remove/', views.session_remove, name='session_remove'),
    path('modal-content/', views.cart_modal_content, name='modal_content'),  # Новый маршрут для получения содержимого модальной корзины
]