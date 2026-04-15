from django import template

register = template.Library()

@register.filter
def split(value, delimiter=' '):
    """Divide un string por el separador dado"""
    if value and isinstance(value, str):
        return value.split(delimiter)
    return []

@register.filter
def last(value):
    """Obtiene el último elemento de una lista"""
    if value and isinstance(value, list) and len(value) > 0:
        return value[-1]
    return ''