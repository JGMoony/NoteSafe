from django import template

register = template.Library()

@register.filter
def dict_get(dictionary, key):
    if dictionary is None:
        return ""

    if isinstance(dictionary, dict):
        return dictionary.get(key, "")

    try:
        return getattr(dictionary, key)
    except AttributeError:
        return ""