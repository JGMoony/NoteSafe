from django import template

register = template.Library()

@register.filter
def dict_get(dictionary, key):
    """
    Permite obtener valores de un diccionario o atributos de un objeto en plantillas.
    Uso en template:
    {{ mi_diccionario|dict_get:"llave" }}
    """
    if dictionary is None:
        return ""

    # Si es diccionario
    if isinstance(dictionary, dict):
        return dictionary.get(key, "")

    # Si es objeto con atributo
    try:
        return getattr(dictionary, key)
    except AttributeError:
        return ""
