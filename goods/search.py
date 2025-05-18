from django.db.models import Manager
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
    SearchHeadline
)
from goods.models import Product

def q_search(query: str) -> Manager[Product]:
    """
    Улучшенная функция полнотекстового поиска товаров с подсветкой совпадений
    
    Args:
        query: Поисковый запрос
        
    Returns:
        QuerySet с результатами поиска, аннотированный:
        - rank (релевантность)
        - highlighted_name (подсветка в названии)
        - highlighted_code (подсветка в коде)
        - highlighted_description (подсветка в описании)
    """
    # Поиск по ID если запрос - число (до 5 цифр)
    if query.isdigit() and len(query) <= 5:
        return Product.objects.filter(id=int(query))

    # Создаем поисковый запрос
    search_query = SearchQuery(query, config='russian')
    
    # Создаем векторы поиска для разных полей
    name_vector = SearchVector('name', config='russian')
    code_vector = SearchVector('code', config='russian')
    desc_vector = SearchVector('description', config='russian')
    
    # Комбинированный вектор для расчета релевантности
    combined_vector = name_vector + code_vector + desc_vector

    # Основной поисковый запрос с аннотациями
    results = (
        Product.objects
        .annotate(
            rank=SearchRank(combined_vector, search_query),
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
            ),
            highlighted_description=SearchHeadline(
                'description',
                search_query,
                start_sel='<span class="search-highlight">',
                stop_sel='</span>',
                config='russian'
            )
        )
        .filter(rank__gte=0.1)  # Порог релевантности
        .order_by('-rank')       # Сортировка по релевантности
    )

    return results