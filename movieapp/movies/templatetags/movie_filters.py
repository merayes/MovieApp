from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Bir sözlükten anahtar ile değer almayı sağlayan filtre."""
    return dictionary.get(key, None)
