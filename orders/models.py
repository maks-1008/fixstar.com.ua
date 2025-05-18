from django.db import models
from users.models import User
from goods.models import Product
import uuid
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import logging
from django.db import transaction

logger = logging.getLogger(__name__)


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    CANCELED = 4

    STATUS_CHOICES = (
        (CREATED, "Створено"),
        (PAID, "Оплачено"),
        (ON_WAY, "В дорозі"),
        (DELIVERED, "Доставлено"),
        (CANCELED, "Скасовано"),
    )

    PAYMENT_CHOICES = (
        ("card", "Оплата картою"),
        ("cash", "Готівкою/картою при отриманні"),
        ("bank", "Оплата на розрахунковий рахунок підприємства"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Номер заказа",
        help_text="Формат: порядковый_номер_за_день.DDMMYY",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Користувач",
    )
    first_name = models.CharField(max_length=100, verbose_name="Ім'я")
    last_name = models.CharField(max_length=100, verbose_name="Прізвище")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон")
    requires_delivery = models.BooleanField(
        default=True, verbose_name="Потрібна доставка"
    )
    delivery_address = models.TextField(
        null=True, blank=True, verbose_name="Адреса доставки"
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default="cash",
        verbose_name="Спосіб оплати",
    )
    status = models.SmallIntegerField(
        default=CREATED, choices=STATUS_CHOICES, verbose_name="Статус замовлення"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    # Поле для отслеживания, было ли уже уменьшено количество товаров
    products_reserved = models.BooleanField(
        default=False,
        verbose_name="Товари зарезервовані",
        help_text="Флаг, указывающий, были ли зарезервированы товары",
    )

    class Meta:
        db_table = "order"
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ("-created_at",)

    def __str__(self):
        return (
            f"Замовлення №{self.order_number or self.id} ({self.get_status_display()})"
        )

    def save(self, *args, **kwargs):
        # Генерируем номер заказа при первом сохранении
        if not self.order_number:
            self.order_number = self.generate_order_number()

        # Сохраняем оригинальный статус для существующего заказа
        if self.pk:
            try:
                original = Order.objects.get(pk=self.pk)
                self._original_status = original.status
                if self._original_status != self.status:
                    logger.info(
                        f"Order {self.pk} status changing from {self._original_status} to {self.status}"
                    )
            except Order.DoesNotExist:
                logger.warning(
                    f"Could not find original order with pk={self.pk} for status tracking"
                )
                self._original_status = self.status
        else:
            # Для нового заказа
            self._original_status = self.status

        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_number():
        today = timezone.now().date()
        today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))

        date_part = today.strftime("%d%m%y")

        # Получаем количество заказов, созданных сегодня
        today_orders_count = Order.objects.filter(created_at__gte=today_start).count()

        # Порядковый номер заказа за день (начиная с 1)
        sequence_number = today_orders_count + 1

        # Формат: порядковый_номер_за_день.DDMMYY
        order_number = f"{sequence_number}.{date_part}"

        return order_number

    def reserve_products(self):
        """Уменьшает количество товаров в наличии при создании заказа"""
        if self.products_reserved:
            logger.warning(
                f"Товары для заказа {self.order_number} уже зарезервированы. Пропускаем."
            )
            return False

        with transaction.atomic():
            for item in self.items.select_related("product").all():
                product = item.product

                initial_quantity = product.quantity

                product.quantity = max(0, product.quantity - item.quantity)

                product.save(update_fields=["quantity"])

                logger.info(
                    f"Резервирование товара: {product.code} - {product.name}. "
                    f"Было: {initial_quantity}, Списано: {item.quantity}, "
                    f"Осталось: {product.quantity}"
                )

            self.products_reserved = True
            self.save(update_fields=["products_reserved"])

            logger.info(
                f"Для заказа {self.order_number} товары успешно зарезервированы"
            )
            return True

    def return_products(self):
        """Возвращает количество товаров при отмене заказа"""
        if not self.products_reserved:
            logger.warning(
                f"Товары для заказа {self.order_number} не были зарезервированы. Пропускаем возврат."
            )
            return False

        with transaction.atomic():
            for item in self.items.select_related("product").all():
                product = item.product

                initial_quantity = product.quantity

                product.quantity += item.quantity

                product.save(update_fields=["quantity"])

                logger.info(
                    f"Возврат товара: {product.code} - {product.name}. "
                    f"Было: {initial_quantity}, Возвращено: {item.quantity}, "
                    f"Стало: {product.quantity}"
                )

            self.products_reserved = False
            self.save(update_fields=["products_reserved"])

            logger.info(
                f"Для заказа {self.order_number} товары успешно возвращены в инвентарь"
            )
            return True

    def get_total_cost(self):
        try:
            return sum(item.get_cost() for item in self.items.all())
        except (TypeError, ValueError):
            return 0

    @property
    def total_items(self):
        try:
            return sum(
                item.quantity for item in self.items.all() if item.quantity is not None
            )
        except (TypeError, ValueError):
            return 0

    def get_status_badge(self):
        badges = {
            self.CREATED: "badge-info",
            self.PAID: "badge-primary",
            self.ON_WAY: "badge-warning",
            self.DELIVERED: "badge-success",
            self.CANCELED: "badge-danger",
        }
        return badges.get(self.status, "badge-secondary")


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE, verbose_name="Замовлення"
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    class Meta:
        db_table = "order_item"
        verbose_name = "Елемент замовлення"
        verbose_name_plural = "Елементи замовлення"
        ordering = ("id",)

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    def get_cost(self):
        if self.price is None or self.quantity is None:
            return 0
        return self.price * self.quantity


# Сигналы для автоматической обработки товаров при изменении статуса заказа
@receiver(post_save, sender=OrderItem)
def process_orderitem_creation(sender, instance, created, **kwargs):
    """Обработка создания элементов заказа"""
    if (
        created
        and instance.order.status == Order.CREATED
        and not instance.order.products_reserved
    ):
        # Если это новый элемент заказа и заказ только что создан, резервируем товары
        # Для batch-создания элементов заказа это будет работать неидеально,
        # поэтому дополнительно вызываем reserve_products в представлении
        try:
            instance.order.reserve_products()
        except Exception as e:
            logger.error(f"Ошибка резервирования товаров: {str(e)}", exc_info=True)


# Отключаем обработчик изменения статуса, так как теперь используем прямой вызов метода return_products в админке
# Закомментированный код оставлен для истории и понимания предыдущей логики
'''
@receiver(pre_save, sender=Order)
def process_order_status_change(sender, instance, **kwargs):
    """Обработка изменения статуса заказа"""
    try:
        # Для новых заказов old_instance не существует
        if instance.pk:
            old_instance = Order.objects.get(pk=instance.pk)

            # Если статус изменился на "Отменен"
            if (
                old_instance.status != Order.CANCELED
                and instance.status == Order.CANCELED
            ):
                logger.info(f"Заказ {instance.order_number} отменен, возвращаем товары")
                instance.return_products()

            # Если статус изменился с "Отменен" на любой другой, резервируем товары снова
            elif (
                old_instance.status == Order.CANCELED
                and instance.status != Order.CANCELED
            ):
                logger.info(
                    f"Заказ {instance.order_number} восстановлен, резервируем товары"
                )
                instance.reserve_products()
    except Order.DoesNotExist:
        # Это новый заказ
        pass
    except Exception as e:
        logger.error(
            f"Ошибка обработки изменения статуса заказа: {str(e)}", exc_info=True
        )
'''


# Добавим функцию для отладки
def debug_order_inventory(order_number):
    """Функция для отладки состояния товаров в заказе"""
    try:
        order = Order.objects.get(order_number=order_number)
        print(
            f"Заказ: {order.order_number}, Статус: {order.get_status_display()}, Товары зарезервированы: {order.products_reserved}"
        )

        for item in order.items.select_related("product").all():
            print(f"  Товар: {item.product.code} - {item.product.name}")
            print(f"  Количество в заказе: {item.quantity}")
            print(f"  Текущее количество на складе: {item.product.quantity}")
            print("  ----------")

        return True
    except Order.DoesNotExist:
        print(f"Заказ с номером {order_number} не найден")
        return False
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return False


class EmailNotificationSettings(models.Model):
    """Модель для хранения настроек электронных уведомлений заказов"""

    name = models.CharField(
        max_length=100,
        verbose_name="Назва налаштування",
        default="Основний",
        help_text="Назва для ідентифікації цього набору налаштувань",
    )
    email = models.TextField(
        verbose_name="Email для повідомлень",
        help_text="Вкажіть email-адреси для отримання повідомлень. Кожну адресу з нового рядка.",
        blank=True,
    )
    is_active = models.BooleanField(
        verbose_name="Активно",
        default=True,
        help_text="Увімкнути або вимкнути відправку повідомлень",
    )

    # Настройки почтового сервера
    smtp_server = models.CharField(
        max_length=100,
        verbose_name="SMTP сервер",
        default="smtp.gmail.com",
        help_text="Адреса SMTP-сервера для відправки листів",
    )
    smtp_port = models.PositiveIntegerField(
        verbose_name="SMTP порт",
        default=587,
        help_text="Порт SMTP-сервера (зазвичай 25, 465 або 587)",
    )
    use_tls = models.BooleanField(
        verbose_name="Використовувати TLS",
        default=True,
        help_text="Використовувати захищене з'єднання TLS",
    )
    sender_email = models.EmailField(
        verbose_name="Email відправника",
        help_text="Email, від імені якого будуть відправлятися повідомлення",
        default="noreply@example.com",
    )
    smtp_username = models.CharField(
        max_length=100,
        verbose_name="Ім'я користувача SMTP",
        help_text="Ім'я користувача для авторизації на SMTP-сервері (зазвичай це email)",
        blank=True,
    )
    smtp_password = models.CharField(
        max_length=100,
        verbose_name="Пароль SMTP",
        help_text="Пароль для авторизації на SMTP-сервері або пароль додатку",
        blank=True,
    )

    # Настройки содержимого письма
    email_subject_template = models.CharField(
        max_length=200,
        verbose_name="Шаблон теми листа",
        default="Нове замовлення №{order_id}",
        help_text="Шаблон теми листа. Використовуйте {order_id} для номера замовлення",
    )
    email_signature = models.TextField(
        verbose_name="Підпис в листі",
        help_text="Підпис, який буде додано в кінці листа",
        default="З повагою,\nКоманда інтернет-магазину",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name = "Налаштування повідомлень"
        verbose_name_plural = "Налаштування повідомлень"

    def __str__(self):
        status = "Активно" if self.is_active else "Неактивно"
        if self.email:
            emails = self.get_emails_list()
            if len(emails) == 1:
                return f"{self.name}: {emails[0]} ({status})"
            return f"{self.name}: {len(emails)} адрес ({status})"
        return f"{self.name}: Повідомлення вимкнено ({status})"

    def get_emails_list(self):
        """Повертає список email-адрес із поля email"""
        if not self.email:
            return []
        return [email.strip() for email in self.email.split("\n") if email.strip()]

    def test_connection(self):
        """Тестирует соединение с SMTP сервером и возвращает результат"""
        try:
            import smtplib

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.ehlo()
            if self.use_tls:
                server.starttls()
                server.ehlo()
            if self.smtp_username and self.smtp_password:
                server.login(self.smtp_username, self.smtp_password)
            server.quit()
            return True, "З'єднання успішно встановлено"
        except Exception as e:
            return False, f"Помилка з'єднання: {str(e)}"

    @classmethod
    def get_active_emails(cls):
        """Повертає список активних email для повідомлень"""
        settings = cls.objects.filter(is_active=True)
        emails = []
        for setting in settings:
            emails.extend(setting.get_emails_list())
        return emails

    @classmethod
    def get_active_settings(cls):
        """Возвращает активные настройки для отправки писем"""
        return cls.objects.filter(is_active=True).first()
