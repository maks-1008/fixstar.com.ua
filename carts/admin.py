from django.contrib import admin
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "quantity",
        "products_price",
        "created_timestamp",
    )
    list_filter = ("user", "created_timestamp")
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "product__name",
    )
    readonly_fields = ("created_timestamp",)
    date_hierarchy = "created_timestamp"

    def products_price(self, obj):
        return obj.products_price()

    products_price.short_description = "Вартість"

    def get_queryset(self, request):
        # Оптимизируем запрос, добавляя предзагрузку связанных моделей
        return super().get_queryset(request).select_related("user", "product")
