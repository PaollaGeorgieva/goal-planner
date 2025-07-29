from django import template

register = template.Library()

@register.filter
def before_at(value):
    """
    Връща частта от стринга преди първия '@'.
    Ако няма '@', връща целия стринг.
    """
    if not isinstance(value, str):
        return value
    return value.split('@')[0]
