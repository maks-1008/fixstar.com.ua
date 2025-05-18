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
        cart_count = len(cart)
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

def cart_change(request, product_id):
    """Изменение количества товара в корзине."""
    print(f"====== cart_change called: product_id={product_id} ======")
    print(f"Request method: {request.method}")
    print(f"POST data: {request.POST}")
    print(f"User authenticated: {request.user.is_authenticated}")
    
    product = get_object_or_404(Product, id=product_id)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            error_msg = "Кількість має бути позитивним числом"
            print(f"Error: {error_msg}")
            if is_ajax:
                return JsonResponse({'success': False, 'message': error_msg})
            messages.error(request, error_msg)
            return redirect(request.META.get('HTTP_REFERER', '/'))
    except (ValueError, TypeError) as e:
        error_msg = "Некоректна кількість товару"
        print(f"Error: {error_msg}, Exception: {str(e)}")
        if is_ajax:
            return JsonResponse({'success': False, 'message': error_msg})
        messages.error(request, error_msg)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # Проверка доступного количества
    if quantity > product.quantity:
        error_msg = f"Недостатньо товару. В наявності: {product.quantity} шт."
        print(f"Error: {error_msg}")
        if is_ajax:
            return JsonResponse({'success': False, 'message': error_msg})
        messages.error(request, error_msg)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # Обновляем количество в корзине
    if request.user.is_authenticated:
        # Получаем объект корзины для авторизованного пользователя
        try:
            cart_item = Cart.objects.get(user=request.user, product=product)
            print(f"Found cart item: id={cart_item.id}, current quantity={cart_item.quantity}")
            
            # Если количество не изменилось, не делаем обновление
            if cart_item.quantity == quantity:
                print("Quantity not changed, returning success response")
                if is_ajax:
                    response_data = {
                        'success': True,
                        'message': "",
                        'item_price': float(cart_item.products_price()),
                        'cart_total': float(Cart.objects.filter(user=request.user).total_price()),
                        'cart_count': Cart.objects.filter(user=request.user).count()
                    }
                    print(f"Response: {response_data}")
                    return JsonResponse(response_data)
                return redirect(request.META.get('HTTP_REFERER', '/'))
                
            # Обновляем количество
            print(f"Updating quantity from {cart_item.quantity} to {quantity}")
            cart_item.quantity = quantity
            cart_item.save()
            
            # Формируем ответ
            if is_ajax:
                response_data = {
                    'success': True,
                    'message': "Кількість товару змінено",
                    'item_price': float(cart_item.products_price()),
                    'cart_total': float(Cart.objects.filter(user=request.user).total_price()),
                    'cart_count': Cart.objects.filter(user=request.user).count()
                }
                print(f"Response: {response_data}")
                return JsonResponse(response_data)
            messages.success(request, "Кількість товару змінено")
            return redirect(request.META.get('HTTP_REFERER', '/'))
            
        except Cart.DoesNotExist:
            error_msg = "Товар не знайдено в кошику"
            print(f"Error: {error_msg}")
            if is_ajax:
                return JsonResponse({
                    'success': False, 
                    'message': error_msg
                })
            messages.error(request, error_msg)
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        # Обработка изменения количества для неавторизованного пользователя
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        
        print(f"Session cart before update: {cart}")
        
        # Если товара нет в корзине или количество не изменилось
        if product_id_str not in cart:
            error_msg = "Товар не знайдено в кошику"
            print(f"Error: {error_msg}")
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'message': error_msg
                })
            messages.error(request, error_msg)
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        if cart[product_id_str] == quantity:
            print("Quantity not changed, returning success response")
            if is_ajax:
                # Вычисляем общую сумму корзины и сумму за данный товар
                total_price = 0
                item_price = 0
                for pid, qty in cart.items():
                    try:
                        p = Product.objects.get(id=int(pid))
                        if pid == product_id_str:
                            item_price = p.price * qty
                        total_price += p.price * qty
                    except (Product.DoesNotExist, ValueError):
                        continue
                
                response_data = {
                    'success': True,
                    'message': "",
                    'item_price': float(item_price),
                    'cart_total': float(total_price),
                    'cart_count': len(cart)
                }
                print(f"Response: {response_data}")
                return JsonResponse(response_data)
            return redirect(request.META.get('HTTP_REFERER', '/'))
            
        # Обновляем корзину
        print(f"Updating quantity from {cart[product_id_str]} to {quantity}")
        cart[product_id_str] = quantity
        request.session['cart'] = cart
        request.session.modified = True
        print(f"Session cart after update: {cart}")
        
        if is_ajax:
            # Вычисляем общую сумму корзины и сумму за данный товар
            total_price = 0
            item_price = 0
            for pid, qty in cart.items():
                try:
                    p = Product.objects.get(id=int(pid))
                    if pid == product_id_str:
                        item_price = p.price * qty
                    total_price += p.price * qty
                except (Product.DoesNotExist, ValueError):
                    continue
                    
            response_data = {
                'success': True,
                'message': "Кількість товару змінено",
                'item_price': float(item_price),
                'cart_total': float(total_price),
                'cart_count': len(cart)
            }
            print(f"Response: {response_data}")
            return JsonResponse(response_data)
            
        messages.success(request, "Кількість товару змінено")
        return redirect(request.META.get('HTTP_REFERER', '/'))

def session_change(request):
    """Изменение количества товара в сессионной корзине."""
    print("====== session_change called ======")
    print(f"Request method: {request.method}")
    print(f"POST data: {request.POST}")
    
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    try:
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        print(f"Product ID: {product_id}, Quantity: {quantity}")
        
        if not product_id or quantity < 1:
            error_msg = "Некорректные данные запроса"
            print(f"Error: {error_msg}")
            if is_ajax:
                return JsonResponse({'success': False, 'message': error_msg})
            messages.error(request, error_msg)
            return redirect(request.META.get('HTTP_REFERER', '/'))
            
        product = get_object_or_404(Product, id=product_id)
        print(f"Found product: {product.name}, Available: {product.quantity}")
        
        # Проверка доступного количества
        if quantity > product.quantity:
            error_msg = f"Недостатньо товару. В наявності: {product.quantity} шт."
            print(f"Error: {error_msg}")
            if is_ajax:
                return JsonResponse({'success': False, 'message': error_msg})
            messages.error(request, error_msg)
            return redirect(request.META.get('HTTP_REFERER', '/'))
            
        cart = request.session.get('cart', {})
        print(f"Session cart before update: {cart}")
        
        # Проверяем, изменилось ли количество
        if product_id in cart and cart[product_id] == quantity:
            print("Quantity not changed, returning success response")
            if is_ajax:
                # Вычисляем общую сумму корзины и сумму за данный товар
                total_price = 0
                item_price = 0
                for pid, qty in cart.items():
                    try:
                        p = Product.objects.get(id=int(pid))
                        if pid == product_id:
                            item_price = p.price * qty
                        total_price += p.price * qty
                    except (Product.DoesNotExist, ValueError):
                        continue
                
                response_data = {
                    'success': True,
                    'message': "",
                    'item_price': float(item_price),
                    'cart_total': float(total_price),
                    'cart_count': len(cart)
                }
                print(f"Response: {response_data}")
                return JsonResponse(response_data)
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        # Обновляем корзину
        print(f"Updating quantity to {quantity}")
        cart[product_id] = quantity
        request.session['cart'] = cart
        request.session.modified = True
        print(f"Session cart after update: {cart}")
        
        if is_ajax:
            # Вычисляем общую сумму корзины и сумму за данный товар
            total_price = 0
            item_price = 0
            for pid, qty in cart.items():
                try:
                    p = Product.objects.get(id=int(pid))
                    if pid == product_id:
                        item_price = p.price * qty
                    total_price += p.price * qty
                except (Product.DoesNotExist, ValueError):
                    continue
                    
            response_data = {
                'success': True,
                'message': "Кількість товару змінено",
                'item_price': float(item_price),
                'cart_total': float(total_price),
                'cart_count': len(cart)
            }
            print(f"Response: {response_data}")
            return JsonResponse(response_data)
            
        messages.success(request, "Кількість товару змінено")
        return redirect(request.META.get('HTTP_REFERER', '/'))
        
    except (ValueError, TypeError) as e:
        error_msg = f"Помилка при зміні кількості: {str(e)}"
        print(f"Error: {error_msg}")
        if is_ajax:
            return JsonResponse({'success': False, 'message': error_msg})
        messages.error(request, error_msg)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    except Product.DoesNotExist:
        error_msg = "Товар не найден"
        print(f"Error: {error_msg}")
        if is_ajax:
            return JsonResponse({'success': False, 'message': error_msg})
        messages.error(request, error_msg)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    except Exception as e:
        error_msg = f"Непередбачена помилка: {str(e)}"
        print(f"Error: {error_msg}")
        if is_ajax:
            return JsonResponse({'success': False, 'message': error_msg})
        messages.error(request, error_msg)
        return redirect(request.META.get('HTTP_REFERER', '/'))

def session_remove(request):
    """Видалення товару із сесійного кошика."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    try:
        product_id = request.POST.get('product_id')
        
        if not product_id:
            if is_ajax:
                return JsonResponse({'success': False, 'message': "Некоректні дані запиту"})
            messages.error(request, "Некоректні дані запиту")
            return redirect(request.META.get('HTTP_REFERER', '/'))
            
        cart = request.session.get('cart', {})
        
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            
            if is_ajax:
                # Вычисляем общую сумму корзины
                total_price = 0
                for pid, qty in cart.items():
                    try:
                        p = Product.objects.get(id=int(pid))
                        total_price += p.price * qty
                    except (Product.DoesNotExist, ValueError):
                        continue
                        
                return JsonResponse({
                    'success': True,
                    'message': "Товар видалено з кошика",
                    'cart_total': float(total_price),
                    'cart_count': len(cart)
                })
                
            messages.success(request, "Товар видалено з кошика")
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'message': "Товар не знайдено в кошику"})
            messages.error(request, "Товар не знайдено в кошику")
            
        return redirect(request.META.get('HTTP_REFERER', '/'))
        
    except Exception as e:
        if is_ajax:
            return JsonResponse({'success': False, 'message': str(e)})
        messages.error(request, str(e))
        return redirect(request.META.get('HTTP_REFERER', '/'))

def cart_remove(request, product_id):
    """Удаление товара из корзины."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.get(user=request.user, product_id=product_id)
            cart_item.delete()
            
            if is_ajax:
                return JsonResponse({
                    'success': True, 
                    'message': "Товар видалено з кошика",
                    'cart_count': Cart.objects.filter(user=request.user).count(),
                    'cart_total': float(Cart.objects.filter(user=request.user).total_price())
                })
                
            messages.success(request, "Товар видалено з кошика")
        except Cart.DoesNotExist:
            if is_ajax:
                return JsonResponse({'success': False, 'message': "Товар не знайдено в кошику"})
            messages.error(request, "Товар не знайдено в кошику")
    else:
        # Обработка для неавторизованных пользователей
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            del cart[product_id_str]
            request.session['cart'] = cart
            
            if is_ajax:
                # Вычисляем общую сумму корзины
                total_price = 0
                for pid, qty in cart.items():
                    try:
                        p = Product.objects.get(id=int(pid))
                        total_price += p.price * qty
                    except (Product.DoesNotExist, ValueError):
                        continue
                        
                return JsonResponse({
                    'success': True,
                    'message': "Товар видалено з кошика",
                    'cart_total': float(total_price),
                    'cart_count': len(cart)
                })
                
            messages.success(request, "Товар видалено з кошика")
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'message': "Товар не знайдено в кошику"})
            messages.error(request, "Товар не знайдено в кошику")
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

def cart_modal_content(request):
    """Возвращает только содержимое корзины для AJAX запросов."""
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        context = {'carts': carts, 'show_buttons': False}
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
        context = {'cart_items': cart_items, 'show_buttons': False}
    
    return render(request, 'carts/includes/cart_content.html', context)

