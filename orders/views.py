from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem
from .forms import OrderForm
from carts.models import Cart
from goods.models import Product
import logging

# Настраиваем логгер
logger = logging.getLogger(__name__)


@transaction.atomic
def create_order(request):
    """
    Создает новый заказ на основе данных из формы и товаров в корзине пользователя
    """
    logger.info("Order creation process started")

    if request.method == "POST":
        logger.info(f"POST data: {request.POST}")
        form = OrderForm(request.POST)
        # Додаткова перевірка: якщо обрано самовивіз (requires_delivery=False), встановлюємо delivery_address=''
        if request.POST.get("requires_delivery") == "False":
            logger.info("Самовивіз обрано, очищаємо адресу доставки")
            post_data = request.POST.copy()
            post_data["delivery_address"] = ""
            form = OrderForm(post_data)
            logger.info(f"Модифіковані дані форми: {post_data}")

        if form.is_valid():
            logger.info("Форма валідна")
            try:
                with transaction.atomic():  # Используем вложенную транзакцию для атомарности
                    # Сохраняем заказ
                    order = form.save(commit=False)

                    # Привязываем пользователя к заказу, если он авторизован
                    if request.user.is_authenticated:
                        order.user = request.user
                        logger.info(f"Associating order with user: {request.user.id}")

                    # Сохраняем заказ, чтобы получить ID
                    order.save()
                    logger.info(f"Order created: {order.id}, status: {order.status}")

                    # Добавляем товары из корзины в заказ
                    cart_items = []
                    if request.user.is_authenticated:
                        # Для авторизованных пользователей получаем корзину из БД
                        carts = Cart.objects.filter(user=request.user).all()
                        if carts:
                            for cart_item in carts:
                                cart_items.append(
                                    {
                                        "product": cart_item.product,
                                        "quantity": cart_item.quantity,
                                    }
                                )
                    else:
                        # Для анонимных пользователей получаем корзину из сессии
                        session_cart = request.session.get("cart", {})
                        for product_id, quantity in session_cart.items():
                            try:
                                product = Product.objects.get(id=int(product_id))
                                cart_items.append(
                                    {"product": product, "quantity": quantity}
                                )
                            except (ValueError, Product.DoesNotExist):
                                continue

                    # Проверяем, что корзина не пуста
                    if not cart_items:
                        messages.error(request, "Ваш кошик порожній")
                        # Выбрасываем исключение, чтобы откатить транзакцию
                        raise ValueError("Cart is empty")

                    # Создаем список для массового создания OrderItem
                    order_items = []
                    for item in cart_items:
                        order_items.append(
                            OrderItem(
                                order=order,
                                product=item["product"],
                                price=item["product"].price,
                                quantity=item["quantity"],
                            )
                        )
                        logger.info(
                            f"Prepared order item: product: {item['product'].id}, quantity: {item['quantity']}"
                        )

                    # Создаем все элементы заказа одновременно
                    OrderItem.objects.bulk_create(order_items)
                    logger.info(f"Created {len(order_items)} order items in bulk")

                    # Явно резервируем товары после создания всех элементов заказа
                    # Это уменьшит количество товаров на складе
                    success = order.reserve_products()
                    if success:
                        logger.info(
                            f"Товары для заказа {order.id} успешно зарезервированы"
                        )
                    else:
                        logger.warning(
                            f"Товары для заказа {order.id} не были зарезервированы. Возможно, они уже были зарезервированы."
                        )

                    # Очищаем корзину после создания всех элементов заказа
                    if request.user.is_authenticated:
                        Cart.objects.filter(user=request.user).delete()
                        logger.info(
                            f"Cleared cart for authenticated user: {request.user.id}"
                        )
                    else:
                        request.session["cart"] = {}
                        logger.info("Cleared session cart for anonymous user")

                    # Отправляем уведомление вручную, так как при bulk_create сигналы не работают
                    from .notifications import send_order_notification
                    from .models import EmailNotificationSettings

                    # Отправка уведомления администраторам
                    notification_emails = EmailNotificationSettings.get_active_emails()
                    if notification_emails:
                        logger.info(
                            f"Sending notifications for order {order.id} to {len(notification_emails)} recipients"
                        )
                        for email in notification_emails:
                            send_result = send_order_notification(
                                order, email, is_admin=True
                            )
                            logger.info(
                                f"Notification to {email}: {'success' if send_result else 'failed'}"
                            )

                    # Отправка уведомления пользователю
                    if request.user.is_authenticated and request.user.email:
                        logger.info(
                            f"Sending notification for order {order.id} to user {request.user.email}"
                        )
                        send_result = send_order_notification(
                            order, request.user.email, is_admin=False
                        )
                        logger.info(
                            f"Notification to user {request.user.email}: {'success' if send_result else 'failed'}"
                        )

                messages.success(
                    request, f"Замовлення №{order.order_number} успішно оформлено!"
                )
                return redirect("main:index")

            except ValueError as e:
                # Пустая корзина обрабатывается выше и перенаправляет пользователя
                if str(e) == "Cart is empty":
                    return redirect("carts:cart_view")

                logger.error(f"Error creating order: {str(e)}")
                messages.error(request, f"Помилка при оформленні замовлення: {str(e)}")
            except Exception as e:
                logger.error(
                    f"Unexpected error creating order: {str(e)}", exc_info=True
                )
                messages.error(request, f"Помилка при оформленні замовлення: {str(e)}")
        else:
            logger.warning(f"Помилки валідації форми: {form.errors}")
            messages.error(request, "Будь ласка, виправте помилки у формі")
    else:
        # GET-запрос
        initial_data = {}
        if request.user.is_authenticated:
            # Предзаполняем форму данными пользователя, если он авторизован
            initial_data = {
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "phone_number": request.user.phone_number,
            }
        form = OrderForm(initial=initial_data)

    # Отображаем страницу оформления заказа
    return render(request, "orders/create_order.html", {"form": form})
