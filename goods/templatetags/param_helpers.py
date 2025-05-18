from django import template
from urllib.parse import parse_qs, urlencode, urlparse, parse_qsl

register = template.Library()

@register.simple_tag
def remove_url_param(url_params, param_name):
    """
    Удаляет параметр из строки GET параметров (для использования в URL)
    """
    if not url_params:
        return ''
    
    # Более надежная обработка параметров
    params = parse_qsl(url_params)
    filtered_params = [(k, v) for k, v in params if k != param_name]
    return urlencode(filtered_params)
 
@register.filter
def remove_param(query_string, param_name):
    """
    Удаляет параметр из строки запроса
    """
    if not query_string:
        return ''
    
    params = parse_qs(query_string)
    if param_name in params:
        del params[param_name]
    
    return urlencode(params, doseq=True)

@register.simple_tag
def update_url_param(url_params, param_name, param_value):
    """
    Обновляет или добавляет параметр в строку GET параметров
    """
    if not url_params:
        return urlencode({param_name: param_value})
    
    params = parse_qsl(url_params)
    # Удаляем старый параметр, если он есть
    params = [(k, v) for k, v in params if k != param_name]
    # Добавляем новый
    params.append((param_name, param_value))
    return urlencode(params)

@register.filter
def add_query_param(query_dict, param_name, param_value):
    """
    Добавляет или обновляет параметр в QueryDict
    """
    params = query_dict.copy()
    params[param_name] = param_value
    return params.urlencode()