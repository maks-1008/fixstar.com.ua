from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order, OrderItem, EmailNotificationSettings
from goods.models import Product
from .notifications import send_order_notification
from django.conf import settings
import logging
from django.db.models import Count
from carts.models import Cart

# Настраиваем логгер
logger = logging.getLogger(__name__)


@receiver(post_save, sender=OrderItem)
def reserve_product_on_order_item_create(sender, instance, created, **kwargs):
    """
    Резервирует товар при создании элемента заказа
    """
    logger.info(
        f"Signal triggered for OrderItem: {instance}, created={created}, order_status={instance.order.status}"
    )

    # Важное изменение: сигнал срабатывает для всех новых OrderItem, независимо от статуса заказа,
    # так как новые заказы всегда создаются со статусом CREATED (0)
    if (
        created
    ):  # Убираем проверку статуса, т.к. модель заказа по умолчанию имеет статус CREATED
        product = instance.product
        logger.info(
            f"Processing product {product.id}, current quantity: {product.quantity}"
        )

        # Проверяем, есть ли поле quantity в модели Product
        if hasattr(product, "quantity"):
            old_quantity = product.quantity
            product.quantity -= instance.quantity
            product.save()
            logger.info(
                f"Product quantity updated: {old_quantity} -> {product.quantity}"
            )
        # Или stock_quantity
        elif hasattr(product, "stock_quantity"):
            old_quantity = product.stock_quantity
            product.stock_quantity -= instance.quantity
            product.save()
            logger.info(
                f"Product stock_quantity updated: {old_quantity} -> {product.stock_quantity}"
            )


@receiver(pre_save, sender=Order)
def handle_order_status_change(sender, instance, **kwargs):
    """
    Обрабатывает изменение статуса заказа
    """
    # Проверяем, существует ли уже этот заказ
    try:
        old_instance = Order.objects.get(pk=instance.pk)
        old_status = old_instance.status
        logger.info(f"Order status change detected: {old_status} -> {instance.status}")

        # Если статус заказа изменился и пользователь авторизован - отправляем уведомление
        if old_status != instance.status and instance.user and instance.user.email:
            logger.info(
                f"Sending status update notification to user: {instance.user.email}"
            )
            # После сохранения модели будет отправлено уведомление (см. send_status_update_notification)

        # Если заказ был отменен
        if old_status != Order.CANCELED and instance.status == Order.CANCELED:
            logger.info(f"Order {instance.id} canceled, returning items to stock")
            # Возвращаем товары в доступный запас
            for item in instance.items.all():
                product = item.product
                logger.info(f"Returning {item.quantity} of product {product.id}")
                if hasattr(product, "quantity"):
                    old_quantity = product.quantity
                    product.quantity += item.quantity
                    product.save()
                    logger.info(
                        f"Product quantity updated: {old_quantity} -> {product.quantity}"
                    )
                elif hasattr(product, "stock_quantity"):
                    old_quantity = product.stock_quantity
                    product.stock_quantity += item.quantity
                    product.save()
                    logger.info(
                        f"Product stock_quantity updated: {old_quantity} -> {product.stock_quantity}"
                    )
    except Order.DoesNotExist:
        # Новый заказ, резервирование происходит в post_save OrderItem
        logger.info(f"New order detected: {instance.id}")
        pass


@receiver(post_save, sender=Order)
def send_status_update_notification(sender, instance, created, **kwargs):
    """
    Отправляет уведомление пользователю при изменении статуса заказа
    (Но не при создании - это делается вручную в представлении)
    """
    # Проверяем, что у пользователя есть email
    if instance.user and instance.user.email:
        # Новые заказы обрабатываются в представлении create_order
        if created:
            logger.info(
                f"New order {instance.id} created, notification handled in view"
            )
            return

        # Если заказ существовал и изменился статус - отправляем уведомление об изменении
        else:
            try:
                # Проверяем, было ли изменение статуса
                old_instance = Order.objects.get(pk=instance.pk)

                # Попытка получить оригинальный статус из атрибута _original_status
                if hasattr(old_instance, "_original_status"):
                    old_status = old_instance._original_status
                    logger.info(
                        f"Retrieved original status from _original_status: {old_status}"
                    )
                else:
                    # Если атрибут не найден, используем текущий статус
                    old_status = old_instance.status
                    logger.warning(
                        f"_original_status not found, using current status: {old_status}"
                    )

                logger.info(
                    f"Checking status change: old={old_status}, new={instance.status}"
                )

                # Сравниваем старый и новый статус
                if old_status != instance.status:
                    logger.info(
                        f"Status changed for order {instance.id}: {old_status} -> {instance.status}. "
                        f"Sending notification to user: {instance.user.email}"
                    )
                    send_result = send_order_notification(
                        instance, instance.user.email, is_admin=False
                    )
                    logger.info(f"Notification sent to user: {send_result}")
                else:
                    logger.info(
                        f"No status change detected for order {instance.id}: {old_status} -> {instance.status}"
                    )
            except Exception as e:
                logger.error(
                    f"Error during status change notification: {e}", exc_info=True
                )
                # Пытаемся отправить уведомление в любом случае, если произошла ошибка при проверке
                try:
                    logger.info(
                        f"Attempting to send notification anyway to: {instance.user.email}"
                    )
                    send_order_notification(
                        instance, instance.user.email, is_admin=False
                    )
                except Exception as inner_e:
                    logger.error(
                        f"Failed to send notification: {inner_e}", exc_info=True
                    )


@receiver(post_save, sender=Order)
def send_order_email_notification(sender, instance, created, **kwargs):
    """
    Отмечает новый заказ для потенциальной отправки уведомления
    DEPRECATED: уведомления теперь отправляются вручную в представлении
    """
    # Отключаем автоматическую отправку, так как теперь это делается вручную
    # в представлении create_order при использовании bulk_create
    if created:
        logger.info(
            f"Order {instance.id} created, but notification is handled in the view"
        )


@receiver(post_save, sender=OrderItem)
def check_order_items_and_send_notification(sender, instance, created, **kwargs):
    """
    DEPRECATED: Проверяет, все ли элементы заказа созданы, и отправляет уведомление
    Этот сигнал больше не используется, так как отправка происходит в представлении
    """
    # Отключаем этот обработчик, чтобы избежать повторных уведомлений
    # Уведомления теперь отправляются непосредственно в представлении create_order
    if created:
        logger.info(
            f"OrderItem {instance.id} created for order {instance.order.id} (notification handled in view)"
        )
    return
