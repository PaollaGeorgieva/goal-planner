from django import template

register = template.Library()

@register.filter
def before_at(value):
    if not isinstance(value, str):
        return value
    return value.split('@')[0]
