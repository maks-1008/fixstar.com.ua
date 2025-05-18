from django.urls import path
from .import views
from .views import search


app_name = 'goods'

urlpatterns = [
    path('search/', search, name='search'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('subcategory/<slug:slug>/', views.subcategory_products, name='subcategory'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]