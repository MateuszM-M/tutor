from django import template

register = template.Library()

@register.filter
def model_name(obj):
    """
    Template filter to get model name
    """
    try:
        return obj._meta.model_name
    except AttributeError:
        return None