from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    Group,
    Permission,
)  # Добавьте эти импорты


class User(AbstractUser):
    image = models.ImageField(
        upload_to="users_images", blank=True, null=True, verbose_name="Аватар"
    )
    phone_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Номер телефону"
    )  # Увеличьте длину до 20

    # Переопределяем метаданные поля username
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Логін",
        help_text="Необхідно. 150 символів або менше. Літери, цифри та @/./+/-/_ лише.",
        error_messages={
            "unique": "Користувач з таким логіном вже існує.",
        },
    )

    class Meta:
        db_table = "users_user"  # Исправьте имя таблицы
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    # Добавьте related_name для избежания конфликтов
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        verbose_name="Групи",
        help_text="Групи, до яких належить користувач.",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        blank=True,
        verbose_name="Права доступу",
        help_text="Специфічні права для цього користувача.",
    )

    @property
    def phone(self):
        return self.phone_number

    @phone.setter
    def phone(self, value):
        self.phone_number = value

    def __str__(self):
        return self.username
