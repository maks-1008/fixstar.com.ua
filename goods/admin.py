from django.contrib import admin
from .models import Category, SubCategory, Product

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget

# Ресурсы для импорта/экспорта
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')

class SubCategoryResource(resources.ModelResource):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'slug')  # 'category' исключен (если не нужен)

class ProductResource(resources.ModelResource):
    subcategory = fields.Field(
        column_name='subcategory',
        attribute='subcategory',
        widget=ForeignKeyWidget(SubCategory, 'name')
    )
    category = fields.Field(column_name='category')  # Добавляем поле category

    class Meta:
        model = Product
        fields = ('id', 'code', 'name', 'slug', 'category', 'subcategory', 'quantity', 'price')

    def dehydrate_category(self, product):
        """Вычисляемое поле: берем категорию из подкатегории."""
        return product.subcategory.category.name if product.subcategory else ""

# Inline для подкатегорий
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    fields = ('name', 'slug', 'category')

# Админка для категорий
@admin.register(Category)
class CategoryAdmin(ImportExportActionModelAdmin):
    resource_class = CategoryResource
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    search_fields = ['name']

# Админка для подкатегорий
@admin.register(SubCategory)
class SubCategoryAdmin(ImportExportActionModelAdmin):
    resource_class = SubCategoryResource
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    search_fields = ['name']

# Админка для товаров
@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'subcategory', 'quantity', 'price')
    list_filter = (
        'subcategory__category',
        'subcategory',
        'quantity',
    )
    search_fields = ['name']