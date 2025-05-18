from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Поля в списке пользователей
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "date_joined",
        "last_login",
        "is_staff",
    )

    # Фильтры в правой части
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        ("date_joined", admin.DateFieldListFilter),
        ("last_login", admin.DateFieldListFilter),
    )

    # Поиск по этим полям
    search_fields = ("username", "email", "phone_number")

    # Порядок полей при редактировании
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Персональна інформація"),
            {"fields": ("first_name", "last_name", "email", "phone_number", "image")},
        ),
        (
            _("Дата"),
            {"fields": ("date_joined", "last_login"), "classes": ("collapse",)},
        ),
        (
            _("Права"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    # Только для чтения (автоматические поля)
    readonly_fields = ("date_joined", "last_login")

    # Порядок полей при создании пользователя
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    # Массовые действия
    actions = ["activate_users", "deactivate_users", "make_staff"]

    def activate_users(self, request, queryset):
        """Активувати вибраних користувачів"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Активовано {updated} користувачів")

    activate_users.short_description = "Активувати вибраних користувачів"

    def deactivate_users(self, request, queryset):
        """Деактивувати вибраних користувачів"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Деактивовано {updated} користувачів")

    deactivate_users.short_description = "Деактивувати вибраних користувачів"

    def make_staff(self, request, queryset):
        """Призначити вибраних користувачів персоналом"""
        if not request.user.is_superuser:
            self.message_user(
                request,
                "Тільки суперкористувачі можуть виконувати цю дію",
                level="error",
            )
            return
        updated = queryset.update(is_staff=True)
        self.message_user(request, f"Назначено {updated} користувачів як персонал")

    make_staff.short_description = "Зробити персоналом (staff)"
