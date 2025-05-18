from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from goods.models import Product  
from carts.models import Cart
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser

@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            if is_ajax:
                return JsonResponse({'success': False, 'message': "Кількість має бути позитивним числом"})
            messages.error(request, "Кількість має бути позитивним числом")
            return redirect(request.META.get('HTTP_REFERER', '/'))
    except (ValueError, TypeError):
        if is_ajax:
            return JsonResponse({'success': False, 'message': "Некоректна кількість товару"})
        messages.error(request, "Некоректна кількість товару")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # Проверка доступного количества
    if quantity > product.quantity:
        error_msg = f"Недостатньо товару. В наявності: {product.quantity} шт."
        if is_ajax:
            return JsonResponse({'success': False, 'message': error_msg})
        messages.error(request, error_msg)
        return redirect(request.META.get('HTTP_REFERER', '/'))

    cart_count = 0

    if isinstance(request.user, AnonymousUser):
        # Обработка для неавторизованных пользователей
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            total_quantity = cart[product_id_str] + quantity
        else:
            total_quantity = quantity
            
        if total_quantity > product.quantity:
            error_msg = f"Не можна додати {quantity} шт. У вас уже {cart.get(product_id_str, 0)} шт. в кошику. Максимум: {product.quantity} шт."
            if is_ajax:
                return JsonResponse({'success': False, 'message': error_msg})
            messages.error(request, error_msg)
            return redirect(request.META.get('HTTP_REFERER', '/'))
            
        cart[product_id_str] = total_quantity
        request.session['cart'] = cart
        
        # Подсчет общего количества товаров в корзине
        cart_count = sum(cart.values())
    else:
        # Обработка для авторизованных пользователей
        existing_cart_item = Cart.objects.filter(user=request.user, product=product).first()
        total_quantity = existing_cart_item.quantity + quantity if existing_cart_item else quantity
        
        if total_quantity > product.quantity:
            error_msg = f"Не можна додати {quantity} шт. У вас вже {existing_cart_item.quantity if existing_cart_item else 0} шт. в кошику. Максимум: {product.quantity} шт."
            if is_ajax:
                return JsonResponse({'success': False, 'message': error_msg})
            messages.error(request, error_msg)
            return redirect(request.META.get('HTTP_REFERER', '/'))

        cart, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart.quantity += quantity
            cart.save()
            
        # Подсчет общего количества товаров в корзине
        cart_count = Cart.objects.filter(user=request.user).count()
    
    success_message = "Товар доданий до кошика"
    if is_ajax:
        return JsonResponse({
            'success': True, 
            'message': success_message,
            'cart_count': cart_count
        })
        
    messages.success(request, success_message)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def cart_view(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        context = {'carts': carts}
    else:
        cart_items = []
        session_cart = request.session.get('cart', {})
        for product_id, quantity in session_cart.items():
            try:
                product = Product.objects.get(id=int(product_id))
                cart_items.append({
                    'product': product,
                    'quantity': quantity
                })
            except (ValueError, Product.DoesNotExist):
                continue
        context = {'cart_items': cart_items}
    
    return render(request, 'carts/cart.html', context)

def cart_change(request, product_slug):
   ...

def cart_remove(request, product_slug):
   ...

