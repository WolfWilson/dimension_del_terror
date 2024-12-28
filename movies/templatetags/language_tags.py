from django import template

register = template.Library()

LANGUAGE_MAPPING = {
    "en": "Inglés",
    "es": "Español",
    "fr": "Francés",
    "de": "Alemán",
    "it": "Italiano",
    "zh": "Chino",
    "ja": "Japonés",
    "ko": "Coreano",
    "ru": "Ruso",
    "pt": "Portugués",
    # Agrega más idiomas si es necesario
}

@register.filter
def translate_language(code):
    """
    Traduce el código de idioma (por ejemplo, 'fr') al nombre completo (por ejemplo, 'Francés').
    """
    return LANGUAGE_MAPPING.get(code, "No disponible")
