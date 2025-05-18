from django.db import models
from goods.models import Product
from users.models import User


class CartQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_items(self):
        """Общее количество товаров (сумма quantity всех позиций)"""
        if self:
            return sum(cart.quantity for cart in self)
        return 0

    def positions_count(self):
        """Количество позиций в корзине (количество разных товаров)"""
        return self.count()


class Cart(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Клієнт",
    )
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, verbose_name="Товар"
    )
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Кількість")
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата додавання"
    )

    class Meta:
        db_table = "cart"
        verbose_name = "Елемент кошика"
        verbose_name_plural = "Кошик покупця"
        ordering = ("id",)

    objects = CartQueryset().as_manager()

    def products_price(self):
        return round(self.product.price * self.quantity, 2)

    def __str__(self):
        if self.user:
            return f"Кошик {self.user.username} | Товар {self.product.name} | Кількість {self.quantity}"

        return (
            f"Анонімний кошик | Товар {self.product.name} | Кількість {self.quantity}"
        )
