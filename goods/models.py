from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex



class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    image = models.ImageField(
        upload_to='category_images/',
        blank=True,
        null=True,
        verbose_name='Зображення категорії'
    )

    class Meta:
        db_table = 'category'
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('goods:category', kwargs={'slug': self.slug})


class SubCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва підкатегорії")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Категорія"
    )
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    image = models.ImageField(
        upload_to='subcategory_images/',
        blank=True,
        null=True,
        verbose_name='Зображення підкатегорії'
    )
    description_image = models.ImageField(
        upload_to='description_images/',
        blank=True,
        null=True,
        verbose_name='Зображення для розширеного опису'
    )

    class Meta:
        db_table = 'subcategory'
        verbose_name = "Підкатегорія"
        verbose_name_plural = "Підкатегорії"
        ordering = ['name']
        unique_together = ['category', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('goods:subcategory', kwargs={'slug': self.slug})


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва товару")
    search_vector = SearchVectorField(null=True, blank=True, editable=False)
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Артикул"
    )
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    strength_class = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Клас міцності"
    )
    coating = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Покриття"
    )
    diameters = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Діаметр, мм"
    )
    cuts = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Крок нарізі, мм"
    )
    lengths = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Довжина, мм"
    )
    price = models.DecimalField(
        default=0.00,
        max_digits=10,
        decimal_places=2,
        verbose_name='Ціна'
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Кількість'
    )
    batch = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Партія"
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Підкатегорія'
    )
    image = models.ImageField(
        upload_to='product_images/',
        blank=True,
        null=True,
        verbose_name='Зображення товару'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Опис товару'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата створення'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата оновлення'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активний товар'
    )
    

    class Meta:
        db_table = 'product'
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ['name']
        indexes = [
            GinIndex(fields=['search_vector']),
            GinIndex(fields=['name'], name='product_name_gin_idx', opclasses=['gin_trgm_ops']),
            models.Index(fields=['code']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.code}-{self.name}")
        super().save(*args, **kwargs)
        Product.objects.filter(pk=self.pk).update(
        search_vector=(
            SearchVector('name', weight='A', config='russian') +
            SearchVector('code', weight='B', config='russian') +
            SearchVector('description', weight='C', config='russian')
        )
    )

    def get_absolute_url(self):
        return reverse('goods:product_detail', kwargs={'slug': self.slug})