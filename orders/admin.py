from django.contrib import admin
from .models import Order, OrderItem, EmailNotificationSettings
from import_export.admin import ImportExportModelAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from .notifications import send_order_notification
import logging
from django.urls import path
from carts.models import Cart
from carts.admin import CartAdmin
from django.db import transaction
from users.models import User

logger = logging.getLogger(__name__)


# Реєструємо Cart у розділі "Замовлення"
@admin.register(Cart)
class CartInOrdersAdmin(CartAdmin):
    """Адміністрування кошика в розділі замовлень"""

    # Пользовательский фильтр для поля user с названием "Користувач"
    class ClientFilter(admin.SimpleListFilter):
        title = "Користувач"  # Отображаемое название фильтра
        parameter_name = "user"  # Имя параметра в URL

        def lookups(self, request, model_admin):
            # Получаем всех уникальных пользователей, у которых есть корзины
            users = User.objects.filter(cart__isnull=False).distinct()
            return [(user.id, f"{user.first_name} {user.last_name}") for user in users]

        def queryset(self, request, queryset):
            # Фильтрация по выбранному пользователю
            if self.value():
                return queryset.filter(user_id=self.value())
            return queryset

    list_display = (
        "get_client",
        "product",
        "quantity",
        "products_price",
        "created_timestamp",
    )
    list_filter = (ClientFilter, "created_timestamp")

    def get_client(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return None

    get_client.short_description = "Користувач"
    get_client.admin_order_field = "user"

    def get_model_perms(self, request):
        """Повертаємо права доступу для моделі"""
        return super().get_model_perms(request)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "price", "quantity", "get_cost")
    fields = ("product", "price", "quantity", "get_cost")
    can_delete = False

    def get_cost(self, obj):
        return obj.get_cost()

    get_cost.short_description = "Сумма"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "created_at",
        "get_client_info",
        "phone_number",
        "status",
        "get_order_total",
        "get_items_count",
    )
    inlines = [OrderItemInline]
    readonly_fields = (
        "id",
        "order_number",
        "created_at",
        "updated_at",
        "get_items_count",
        "get_order_total",
        "user",
    )
    list_filter = ("status", "created_at")

    # Пользовательский фильтр для поля user
    class UserFilter(admin.SimpleListFilter):
        title = "Користувач"  # Отображаемое название фильтра
        parameter_name = "user"  # Имя параметра в URL

        def lookups(self, request, model_admin):
            # Получаем всех уникальных пользователей, у которых есть заказы
            users = User.objects.filter(order__isnull=False).distinct()
            return [(user.id, f"{user.first_name} {user.last_name}") for user in users]

        def queryset(self, request, queryset):
            # Фильтрация по выбранному пользователю
            if self.value():
                return queryset.filter(user_id=self.value())
            return queryset

    list_filter = (UserFilter, "status", "created_at")

    def get_order_total(self, obj):
        return f"{obj.get_total_cost()} грн."

    get_order_total.short_description = "Сума замовлення"

    def get_items_count(self, obj):
        return obj.items.count()

    get_items_count.short_description = "Кількість товарів"

    def get_client_info(self, obj):
        if obj.user:
            url = reverse("admin:users_user_change", args=[obj.user.id])
            return format_html(
                '<a href="{}">{} {}</a>', url, obj.first_name, obj.last_name
            )
        return f"{obj.first_name} {obj.last_name}"

    get_client_info.short_description = "Користувач"

    # Методы для изменения статуса заказов
    def set_status_paid(self, request, queryset):
        """Меняет статус заказа на 'Оплачено'"""
        for order in queryset:
            # Сохраняем оригинальный статус перед изменением
            old_status = order.status
            # Обновляем статус
            order.status = Order.PAID
            order.save()

            # Отправляем уведомление пользователю, если он существует и имеет email
            if order.user and order.user.email:
                logger.info(
                    f"Sending status update notification for order {order.id} to {order.user.email}"
                )
                send_order_notification(order, order.user.email, is_admin=False)

        self.message_user(
            request, f"Змінено статус для {queryset.count()} замовлень на 'Оплачено'"
        )

    set_status_paid.short_description = "Змінити статус на 'Оплачено'"

    def set_status_on_way(self, request, queryset):
        """Меняет статус заказа на 'В дорозі'"""
        for order in queryset:
            # Сохраняем оригинальный статус перед изменением
            old_status = order.status
            # Обновляем статус
            order.status = Order.ON_WAY
            order.save()

            # Отправляем уведомление пользователю, если он существует и имеет email
            if order.user and order.user.email:
                logger.info(
                    f"Sending status update notification for order {order.id} to {order.user.email}"
                )
                send_order_notification(order, order.user.email, is_admin=False)

        self.message_user(
            request, f"Змінено статус для {queryset.count()} замовлень на 'В дорозі'"
        )

    set_status_on_way.short_description = "Змінити статус на 'В дорозі'"

    def set_status_delivered(self, request, queryset):
        """Меняет статус заказа на 'Доставлено'"""
        for order in queryset:
            # Сохраняем оригинальный статус перед изменением
            old_status = order.status
            # Обновляем статус
            order.status = Order.DELIVERED
            order.save()

            # Отправляем уведомление пользователю, если он существует и имеет email
            if order.user and order.user.email:
                logger.info(
                    f"Sending status update notification for order {order.id} to {order.user.email}"
                )
                send_order_notification(order, order.user.email, is_admin=False)

        self.message_user(
            request, f"Змінено статус для {queryset.count()} замовлень на 'Доставлено'"
        )

    set_status_delivered.short_description = "Змінити статус на 'Доставлено'"

    def set_status_canceled(self, request, queryset):
        """Меняет статус заказа на 'Скасовано' и возвращает товары в инвентарь"""
        # Для каждого заказа проверяем, нужно ли вернуть товары
        canceled_count = 0
        returned_items = []

        for order in queryset:
            try:
                # Начинаем транзакцию для каждого заказа
                with transaction.atomic():
                    # Если заказ не был отменен ранее
                    if order.status != Order.CANCELED:
                        # Логируем состояние заказа до отмены
                        logger.info(
                            f"Отмена заказа {order.order_number}: текущий статус={order.get_status_display()}, "
                            f"товары зарезервированы={order.products_reserved}"
                        )

                        # Список товаров для отображения админу
                        order_items = []

                        # Сначала возвращаем товары, если они были зарезервированы
                        if order.products_reserved:
                            try:
                                # Возвращаем товары
                                success = order.return_products()

                                if success:
                                    # Собираем информацию о возвращенных товарах
                                    for item in order.items.select_related(
                                        "product"
                                    ).all():
                                        order_items.append(
                                            f"{item.product.name} ({item.quantity} шт.)"
                                        )
                                        returned_items.append(
                                            (
                                                order.order_number,
                                                item.product.name,
                                                item.quantity,
                                            )
                                        )

                                    logger.info(
                                        f"Товары для заказа {order.order_number} успешно возвращены"
                                    )
                                else:
                                    logger.warning(
                                        f"Не удалось вернуть товары для заказа {order.order_number}"
                                    )
                            except Exception as e:
                                logger.error(
                                    f"Ошибка при возврате товаров для заказа {order.order_number}: {str(e)}"
                                )
                                self.message_user(
                                    request,
                                    f"Ошибка при возврате товаров для заказа {order.order_number}: {str(e)}",
                                    level=messages.ERROR,
                                )

                        # Меняем статус на "Отменен"
                        order.status = Order.CANCELED
                        order.save(update_fields=["status"])

                        # Отправляем уведомление пользователю, если он существует и имеет email
                        if order.user and order.user.email:
                            logger.info(
                                f"Sending status update notification for cancelled order {order.id} to {order.user.email}"
                            )
                            send_order_notification(
                                order, order.user.email, is_admin=False
                            )

                        # Увеличиваем счетчик отмененных заказов
                        canceled_count += 1

                        # Отправляем информацию админу о каждом отмененном заказе
                        if order_items:
                            items_info = ", ".join(order_items)
                            self.message_user(
                                request,
                                f"Заказ №{order.order_number} отменен. Возвращены товары: {items_info}",
                                level=messages.SUCCESS,
                            )
                        else:
                            self.message_user(
                                request,
                                f"Заказ №{order.order_number} отменен. Товары не были зарезервированы.",
                                level=messages.INFO,
                            )
            except Exception as e:
                logger.error(
                    f"Ошибка при отмене заказа {order.order_number}: {str(e)}",
                    exc_info=True,
                )
                self.message_user(
                    request,
                    f"Ошибка при отмене заказа {order.order_number}: {str(e)}",
                    level=messages.ERROR,
                )

        # Общее сообщение об отмененных заказах
        if canceled_count > 0:
            self.message_user(
                request, f"Змінено статус для {canceled_count} замовлень на 'Скасовано'"
            )

            # Итоговая информация о всех возвращенных товарах
            if returned_items:
                summary = "<br>".join(
                    [
                        f"Заказ №{order_num}: {product_name} ({quantity} шт.)"
                        for order_num, product_name, quantity in returned_items
                    ]
                )
                self.message_user(
                    request, f"Возвращены товары:<br>{summary}", level=messages.INFO
                )
        else:
            self.message_user(
                request,
                "Ни один заказ не был отменен. Возможно, они уже имеют статус 'Скасовано'.",
                level=messages.WARNING,
            )

    set_status_canceled.short_description = "Змінити статус на 'Скасовано'"

    actions = [
        "set_status_paid",
        "set_status_on_way",
        "set_status_delivered",
        "set_status_canceled",
    ]

    def save_model(self, request, obj, form, change):
        """Обрабатывает сохранение модели заказа в админке"""
        # Если это изменение существующего заказа
        if change:
            # Проверяем, изменился ли статус заказа
            try:
                original_obj = self.model.objects.get(pk=obj.pk)
                if original_obj.status != obj.status:
                    logger.info(
                        f"Admin detected status change from {original_obj.status} to {obj.status} for order {obj.pk}"
                    )

                    # Сохраняем модель
                    super().save_model(request, obj, form, change)

                    # Отправляем уведомление пользователю после сохранения
                    if obj.user and obj.user.email:
                        logger.info(
                            f"Manually sending notification to user {obj.user.email} for order {obj.pk}"
                        )
                        send_order_notification(obj, obj.user.email, is_admin=False)
                    return
            except self.model.DoesNotExist:
                pass

        # Если статус не изменился или это новый заказ - просто сохраняем
        super().save_model(request, obj, form, change)


@admin.register(EmailNotificationSettings)
class EmailNotificationSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email_preview",
        "recipient_count",
        "is_active",
        "smtp_server",
        "updated_at",
    )
    list_filter = ("is_active", "use_tls")
    search_fields = ("name", "email", "smtp_server", "sender_email")
    fieldsets = (
        (
            "Основні налаштування",
            {
                "fields": ("name", "email", "is_active"),
                "description": "Основні налаштування для отримання повідомлень",
            },
        ),
        (
            "Налаштування SMTP-сервера",
            {
                "fields": (
                    "smtp_server",
                    "smtp_port",
                    "use_tls",
                    "sender_email",
                    "smtp_username",
                    "smtp_password",
                ),
                "description": "Налаштування підключення до SMTP-сервера для відправки листів",
            },
        ),
        (
            "Налаштування вмісту листа",
            {
                "fields": (
                    "email_subject_template",
                    "email_signature",
                ),
                "description": "Налаштування шаблонів і форматування листів",
            },
        ),
        (
            "Службова інформація",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")

    def email_preview(self, obj):
        """Показывает первые email-адреса с ограничением длины"""
        emails = obj.get_emails_list()
        if not emails:
            return "—"

        if len(emails) == 1:
            return emails[0]

        preview = ", ".join(emails[:2])
        if len(emails) > 2:
            preview += f" та ще {len(emails) - 2}"
        return preview

    email_preview.short_description = "Email адреси"

    def recipient_count(self, obj):
        """Показывает количество получателей"""
        count = len(obj.get_emails_list())
        return count

    recipient_count.short_description = "Кількість отримувачів"

    def has_delete_permission(self, request, obj=None):
        # Разрешаем удаление настроек
        return True

    def save_model(self, request, obj, form, change):
        """Тестирует соединение при сохранении, если изменились настройки SMTP"""
        smtp_fields = {
            "smtp_server",
            "smtp_port",
            "use_tls",
            "smtp_username",
            "smtp_password",
        }

        # Если изменились настройки SMTP
        if change and any(field in form.changed_data for field in smtp_fields):
            success, message = obj.test_connection()
            if success:
                messages.success(request, message)
            else:
                messages.warning(request, message)

        super().save_model(request, obj, form, change)

    def get_urls(self):
        """Добавляет URL для тестирования соединения"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/test-connection/",
                self.admin_site.admin_view(self.test_connection_view),
                name="orders_emailnotificationsettings_test_connection",
            ),
        ]
        return custom_urls + urls

    def test_connection_view(self, request, object_id):
        """Обработчик для тестирования соединения"""
        obj = self.get_object(request, object_id)

        if obj is None:
            messages.error(request, "Налаштування не знайдено")
            return HttpResponseRedirect(
                reverse("admin:orders_emailnotificationsettings_changelist")
            )

        success, message = obj.test_connection()
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return HttpResponseRedirect(
            reverse("admin:orders_emailnotificationsettings_change", args=[object_id])
        )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Добавляет кнопку тестирования в форму редактирования"""
        extra_context = extra_context or {}
        extra_context["test_connection_url"] = reverse(
            "admin:orders_emailnotificationsettings_test_connection", args=[object_id]
        )
        return super().change_view(request, object_id, form_url, extra_context)
