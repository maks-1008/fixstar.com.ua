from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, SubCategory, Product
from django.core.cache import cache
from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from .search import q_search
import re
import json

# Константы
CACHE_TIMEOUT = 60 * 60 * 24  # 24 часа кэширования
FILTER_FIELDS = ['strength_class', 'coating', 'diameter', 'lengths']
ITEMS_PER_PAGE = 25

def normalize_search_term(term):
    """Нормализация поискового запроса (M -> М)"""
    return term.replace('M', 'М').replace('m', 'м').strip()

def get_cached_filters(subcategory):
    """Получение закэшированных фильтров для подкатегории"""
    cache_key = f"subcat_filters_{subcategory.id}"
    cached_data = cache.get(cache_key)
    
    if not cached_data:
        products = Product.objects.filter(subcategory=subcategory)
        
        # Диаметры с обработкой M/М
        diameters = products.exclude(diameters__isnull=True)\
                          .values_list('diameters', flat=True)\
                          .distinct()
        diameters = {d.strip().upper().replace('M', 'М') for d in diameters if d}
        
        cached_data = {
            'strength_classes': get_sorted_values(products, 'strength_class', numeric_sort=True),
            'coatings': get_sorted_values(products, 'coating'),
            'diameters': sorted(diameters, key=lambda x: float(x[1:]) if x.startswith('М') else float(x)),
            'lengths': get_sorted_values(products, 'lengths', numeric_sort=True),
        }
        cache.set(cache_key, cached_data, CACHE_TIMEOUT)
    
    return cached_data

def get_sorted_values(queryset, field_name, numeric_sort=False):
    """Универсальная функция для получения и сортировки значений"""
    values = queryset.exclude(**{f"{field_name}__isnull": True})\
                   .values_list(field_name, flat=True)\
                   .distinct()
    values = [v.strip() for v in values if v and str(v).strip()]
    
    if numeric_sort:
        try:
            return sorted(list(set(values)), key=lambda x: float(x))
        except ValueError:
            return sorted(list(set(values)))
    return sorted(list(set(values)))

def apply_product_filters(queryset, get_params):
    """Применение фильтров с учетом M/М"""
    for field in FILTER_FIELDS:
        value = get_params.get(field)
        if value and value != 'None':
            filter_field = 'diameters' if field == 'diameter' else field
            normalized_value = normalize_search_term(value)
            queryset = queryset.filter(
                Q(**{f"{filter_field}__iexact": value}) |
                Q(**{f"{filter_field}__iexact": normalized_value})
            )
    return queryset

from django.contrib.postgres.search import SearchHeadline  # Добавить в импорты

def search(request):
    query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page', 1)
    
    if not query:
        products = Product.objects.none()
    else:
        normalized_query = normalize_search_term(query)
        
        # Сначала пробуем полнотекстовый поиск
        search_query = SearchQuery(query, config='russian')
        products = Product.objects.annotate(
            search=SearchVector('name', 'code', config='russian'),
            highlighted_name=SearchHeadline(
                'name',
                search_query,
                start_sel='<span class="search-highlight">',
                stop_sel='</span>',
                config='russian'
            ),
            highlighted_code=SearchHeadline(
                'code',
                search_query,
                start_sel='<span class="search-highlight">',
                stop_sel='</span>',
                config='russian'
            )
        ).filter(search=search_query)
        
        # Если нет результатов или запрос содержит только цифры - используем частичный поиск
        if not products.exists() or query.isdigit():
            products = Product.objects.filter(
                Q(code__icontains=query) | 
                Q(code__icontains=normalized_query) |
                Q(name__icontains=query) |
                Q(name__icontains=normalized_query)
            )
            
            # Вручную добавляем подсветку для частичных совпадений с учетом регистра и нормализации
            for product in products:
                # Для кода
                original_code = product.code
                normalized_code = normalize_search_term(original_code)
                
                # Ищем все варианты (оригинальный запрос, нормализованный, в разных регистрах)
                for variant in [query, normalized_query, query.lower(), query.upper()]:
                    if variant in original_code:
                        product.highlighted_code = original_code.replace(
                            variant, 
                            f'<span class="search-highlight">{variant}</span>'
                        )
                        break
                    elif variant in normalized_code:
                        product.highlighted_code = normalized_code.replace(
                            variant, 
                            f'<span class="search-highlight">{variant}</span>'
                        )
                        break
                else:
                    product.highlighted_code = original_code
                
                # Для названия
                original_name = product.name
                normalized_name = normalize_search_term(original_name)
                
                for variant in [query, normalized_query, query.lower(), query.upper()]:
                    if variant in original_name:
                        product.highlighted_name = original_name.replace(
                            variant, 
                            f'<span class="search-highlight">{variant}</span>'
                        )
                        break
                    elif variant in normalized_name:
                        product.highlighted_name = normalized_name.replace(
                            variant, 
                            f'<span class="search-highlight">{variant}</span>'
                        )
                        break
                else:
                    product.highlighted_name = original_name
    
    paginator = Paginator(products, ITEMS_PER_PAGE)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'search_performed': bool(query),
    }
    return render(request, 'goods/search_results.html', context)

def product_detail(request, slug):
    """Детальная страница товара с похожими товарами"""
    product = get_object_or_404(
        Product.objects.select_related('subcategory__category'),
        slug=slug
    )
    
    # Похожие товары (из той же подкатегории)
    similar_products = Product.objects.filter(
        subcategory=product.subcategory
    ).exclude(id=product.id)[:4]
    
    return render(request, 'goods/product_detail.html', {
        'product': product,
        'similar_products': similar_products
    })

def category_detail(request, slug):
    """Страница категории с кэшированием"""
    cache_key = f"category_{slug}"
    cached_data = cache.get(cache_key)
    
    if not cached_data:
        category = get_object_or_404(
            Category.objects.prefetch_related('subcategories'),
            slug=slug
        )
        cached_data = {
            'category': category,
            'subcategories': category.subcategories.all()
        }
        cache.set(cache_key, cached_data, CACHE_TIMEOUT)
    
    return render(request, 'goods/category_detail.html', cached_data)

def subcategory_products(request, slug):
    """Товары подкатегории с интеллектуальными фильтрами"""
    subcategory = get_object_or_404(SubCategory, slug=slug)
    cached_filters = get_cached_filters(subcategory)
    
    # Основной queryset
    products = Product.objects.filter(subcategory=subcategory)
    
    # Применяем фильтры
    get_params = request.GET.copy()
    products = apply_product_filters(products, get_params)
    
    # Проверяем, является ли это AJAX запросом
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # Если это AJAX запрос только для длин, возвращаем JSON с доступными длинами
    if request.GET.get('get_lengths_only') == '1' and is_ajax:
        active_filters = {k: v for k, v in get_params.items() if k in FILTER_FIELDS and k != 'lengths'}
        if active_filters:
            filtered_products = Product.objects.filter(subcategory=subcategory)
            filtered_products = apply_product_filters(filtered_products, active_filters)
            filtered_lengths = get_sorted_values(filtered_products, 'lengths', numeric_sort=True)
        else:
            filtered_lengths = cached_filters['lengths']
        
        return JsonResponse({
            'status': 'success',
            'lengths': filtered_lengths,
            'message': f'Найдено {len(filtered_lengths)} длин для выбранных фильтров'
        })
    
    # Получаем длины с учетом всех активных фильтров, кроме lengths
    active_filters = {k: v for k, v in get_params.items() if k in FILTER_FIELDS and k != 'lengths'}
    if active_filters:
        filtered_products = Product.objects.filter(subcategory=subcategory)
        filtered_products = apply_product_filters(filtered_products, active_filters)
        filtered_lengths = get_sorted_values(filtered_products, 'lengths', numeric_sort=True)
    else:
        filtered_lengths = cached_filters['lengths']
    
    # Удаляем активные фильтры при повторном клике
    for field in FILTER_FIELDS:
        param_value = get_params.get(field)
        if param_value and param_value == request.GET.get(field):
            del get_params[field]
    
    # Пагинация
    paginator = Paginator(products, ITEMS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'subcategory': subcategory,
        'page_obj': page_obj,
        'strength_classes': {sc: sc for sc in cached_filters['strength_classes']},
        'coatings': cached_filters['coatings'],
        'diameters': cached_filters['diameters'],
        'lengths': filtered_lengths,  # Используем отфильтрованные длины
        'current_filters': get_params.urlencode(),
        'active_filters': {k: v for k, v in request.GET.items() if k in FILTER_FIELDS and v},
        'products_count': products.count(),
    }
    
    # Для AJAX запросов возвращаем только HTML содержимое с дополнительным заголовком
    if is_ajax:
        response = render(request, 'goods/subcategory_detail.html', context)
        response['X-Is-Ajax-Response'] = 'true'
        response['X-Product-Count'] = str(products.count())
        response['X-Current-Page'] = str(page_obj.number)
        response['X-Total-Pages'] = str(paginator.num_pages)
        return response
    
    return render(request, 'goods/subcategory_detail.html', context)

# Сигналы для очистки кэша
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver([post_save, post_delete], sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    """Очистка кэша при изменении товаров"""
    if hasattr(instance, 'subcategory'):
        cache.delete(f"subcat_filters_{instance.subcategory.id}")
    cache.delete_pattern("category_*")  # Очищаем кэш категорий

@receiver([post_save, post_delete], sender=SubCategory)
def clear_subcategory_cache(sender, instance, **kwargs):
    """Очистка кэша при изменении подкатегорий"""
    cache.delete(f"subcat_filters_{instance.id}")
    cache.delete_pattern("category_*")

@receiver([post_save, post_delete], sender=Category)
def clear_category_cache(sender, instance, **kwargs):
    """Очистка кэша при изменении категорий"""
    cache.delete_pattern("category_*")