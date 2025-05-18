from django import forms
from .models import Order
import logging

logger = logging.getLogger(__name__)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "requires_delivery",
            "delivery_address",
            "payment_method",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Установка обязательных полей
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["phone_number"].required = True
        self.fields["delivery_address"].required = False

        # Добавление атрибутов полям
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

        # Специфичные атрибуты для полей
        self.fields["delivery_address"].widget.attrs["rows"] = 2
        self.fields["requires_delivery"].widget.attrs["class"] = "form-check-input"
        self.fields["payment_method"].widget.attrs["class"] = "form-select"

    def clean(self):
        cleaned_data = super().clean()
        requires_delivery = cleaned_data.get("requires_delivery")
        delivery_address = cleaned_data.get("delivery_address")

        logger.info(
            f"Валідація форми: requires_delivery={requires_delivery}, delivery_address={delivery_address}"
        )

        # Перевіряємо наявність адреси тільки якщо обрана доставка
        if requires_delivery and not delivery_address:
            logger.warning("Помилка валідації: обрана доставка, але адреса не вказана")
            self.add_error("delivery_address", "Вкажіть адресу доставки")
        elif not requires_delivery:
            logger.info("Самовивіз обрано, адреса не потрібна")
            # Якщо самовивіз, встановлюємо порожню адресу
            cleaned_data["delivery_address"] = ""

        return cleaned_data
