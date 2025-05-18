from django.core.mail import send_mail, EmailMessage, get_connection
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from .models import EmailNotificationSettings

# Настраиваем логгер
logger = logging.getLogger(__name__)


def send_order_notification(order, recipient_email=None, is_admin=False):
    """
    Отправляет уведомление о заказе на указанный email.
    Если email не указан, ничего не отправляем.

    Args:
        order: Заказ, о котором отправляем уведомление
        recipient_email: Email получателя
        is_admin: Флаг, указывающий, что получатель - администратор (для выбора шаблона)
    """
    logger.info(f"Starting email notification process for order {order.id}")

    if not recipient_email:
        logger.warning("No recipient email provided, notification will not be sent")
        return False  # Если нет адреса, не отправляем

    try:
        # Получаем активные настройки почты
        mail_settings = EmailNotificationSettings.get_active_settings()

        if not mail_settings:
            logger.warning(
                "No active email settings found, using default email settings"
            )
            # Используем стандартные настройки из settings.py
            return send_order_notification_default(order, recipient_email, is_admin)

        logger.info(f"Using email settings: {mail_settings.name}")

        # Получаем все товары в заказе
        order_items = order.items.all()
        logger.info(f"Order {order.id} has {order_items.count()} items")

        # Получаем URL сайта
        site_url = getattr(settings, "SITE_URL", "http://127.0.0.1:8000")
        logger.info(f"Using site URL: {site_url}")

        # Формируем контекст для шаблона
        context = {
            "order": order,
            "order_items": order_items,
            "total_cost": order.get_total_cost(),
            "admin_url": f"{site_url}/admin/orders/order/{order.id}/change/",
            "site_url": site_url,
            "status_display": order.get_status_display(),
            "signature": mail_settings.email_signature,
        }

        # Выбираем шаблон в зависимости от того, кому отправляем
        template_name = "orders/email/order_notification.html"  # для админа
        if not is_admin and order.user and order.user.email == recipient_email:
            template_name = (
                "orders/email/user_order_notification.html"  # для пользователя
            )

        # Рендерим HTML-сообщение из шаблона (если он есть)
        try:
            logger.info(f"Attempting to render email template: {template_name}")
            html_message = render_to_string(template_name, context)
            plain_message = strip_tags(html_message)
            logger.info("Email template rendered successfully")
        except Exception as template_error:
            logger.error(f"Error rendering template: {template_error}")
            # Если шаблона нет, формируем простое текстовое сообщение
            items_text = "\n".join(
                [
                    f"- {item.product.name}: {item.quantity} шт. x {item.price} = {item.get_cost()}"
                    for item in order_items
                ]
            )
            plain_message = f"""
Нове замовлення №{order.id}

Ім'я: {order.first_name}
Прізвище: {order.last_name}
Телефон: {order.phone_number}
Статус: {order.get_status_display()}
Дата створення: {order.created_at}

Товари:
{items_text}

Загальна сума: {order.get_total_cost()}

Адреса доставки: {order.delivery_address or 'Не вказана'}

{mail_settings.email_signature}
"""
            html_message = plain_message.replace("\n", "<br>")
            logger.info("Fallback to plain text email")

        # Формируем тему письма с учетом статуса заказа
        if not is_admin and order.user and order.user.email == recipient_email:
            # Для пользователя
            order_status = order.get_status_display()
            subject = f"Ваше замовлення №{order.order_number} - {order_status}"
        else:
            # Для администратора
            subject = mail_settings.email_subject_template.format(order_id=order.id)

        # Создаем соединение с SMTP-сервером на основе настроек
        logger.info(
            f"Connecting to SMTP server: {mail_settings.smtp_server}:{mail_settings.smtp_port}"
        )
        connection = get_connection(
            backend="django.core.mail.backends.smtp.EmailBackend",
            host=mail_settings.smtp_server,
            port=mail_settings.smtp_port,
            username=mail_settings.smtp_username,
            password=mail_settings.smtp_password,
            use_tls=mail_settings.use_tls,
            fail_silently=False,
        )

        # Создаем и отправляем письмо
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=mail_settings.sender_email,
            to=[recipient_email],
            connection=connection,
        )
        email.content_subtype = "html"  # Устанавливаем тип содержимого как HTML

        logger.info(f"Sending email to {recipient_email} with subject '{subject}'")
        email.send(fail_silently=False)

        logger.info(
            f"Email notification for order {order.id} sent successfully to {recipient_email}"
        )
        return True
    except Exception as e:
        logger.error(f"Error sending email notification: {e}", exc_info=True)
        return False


def send_order_notification_default(order, recipient_email, is_admin=False):
    """
    Отправляет уведомление о заказе, используя настройки из settings.py.
    Используется как запасной вариант, если нет активных настроек EmailNotificationSettings.
    """
    try:
        # Получаем все товары в заказе
        order_items = order.items.all()

        # Получаем URL сайта
        site_url = getattr(settings, "SITE_URL", "http://127.0.0.1:8000")

        # Формируем контекст для шаблона
        context = {
            "order": order,
            "order_items": order_items,
            "total_cost": order.get_total_cost(),
            "admin_url": f"{site_url}/admin/orders/order/{order.id}/change/",
            "site_url": site_url,
            "status_display": order.get_status_display(),
        }

        # Выбираем шаблон в зависимости от того, кому отправляем
        template_name = "orders/email/order_notification.html"  # для админа
        if not is_admin and order.user and order.user.email == recipient_email:
            template_name = (
                "orders/email/user_order_notification.html"  # для пользователя
            )

        # Рендерим HTML-сообщение из шаблона
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)

        # Формируем тему письма с учетом статуса заказа
        if not is_admin and order.user and order.user.email == recipient_email:
            # Для пользователя
            order_status = order.get_status_display()
            subject = f"Ваше замовлення №{order.order_number} - {order_status}"
        else:
            # Для администратора
            subject = f"Нове замовлення №{order.id}"

        # Отправляем сообщение через стандартные настройки Django
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )

        logger.info(
            f"Email notification (default settings) for order {order.id} sent to {recipient_email}"
        )
        return True
    except Exception as e:
        logger.error(f"Error sending default email notification: {e}", exc_info=True)
        return False
