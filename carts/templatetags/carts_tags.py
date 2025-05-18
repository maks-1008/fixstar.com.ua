from django import template
from goods.models import Product
from django.contrib.auth.models import AnonymousUser
from carts.models import Cart
import json

register = template.Library()

@register.simple_tag
def user_carts(request):
    """Возвращает корзину для авторизованного пользователя"""
    if isinstance(request.user, AnonymousUser):
        return Cart.objects.none()
    return Cart.objects.filter(user=request.user).select_related('product')

@register.filter
def get_product(product_id):
    """Получает продукт по ID с обработкой ошибок"""
    try:
        return Product.objects.get(id=int(product_id))
    except (ValueError, Product.DoesNotExist, TypeError):
        return None

@register.simple_tag
def calculate_session_cart_total(session_cart):
    """Вычисляет общую стоимость корзины в сессии"""
    if not session_cart:
        return 0
        
    try:
        # Обработка случая, когда корзина может быть строкой JSON
        if isinstance(session_cart, str):
            cart_data = json.loads(session_cart)
        else:
            cart_data = session_cart
            
        total = 0
        for product_id, quantity in cart_data.items():
            try:
                product = Product.objects.get(id=int(product_id))
                total += product.price * int(quantity)
            except (ValueError, Product.DoesNotExist, TypeError):
                continue
        return total
    except (AttributeError, ValueError, json.JSONDecodeError):
        return 0

@register.filter
def cart_quantity(cart_dict):
    """Возвращает количество уникальных позиций в корзине сессии"""
    return len(cart_dict) if cart_dict else 0

@register.filter
def multiply(value, arg):
    """Умножает значение на аргумент"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0