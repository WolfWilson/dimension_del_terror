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
    "sv": "Sueco",
    "fi": "Finés",
    "hi": "Hindi",
    "ar": "Árabe",
}

@register.filter
def translate_language(code):
    """
    Traduce el código de idioma (por ejemplo, 'fr') al nombre completo (por ejemplo, 'Francés').
    """
    return LANGUAGE_MAPPING.get(code, "No disponible")

@register.filter
def format_duration(minutes):
    """
    Convierte la duración de minutos a un formato más legible (e.g., "2h 30m").
    """
    if not minutes:
        return "N/A"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m" if hours > 0 else f"{mins}m"

@register.filter
def rating_stars(rating):
    """
    Convierte un puntaje numérico en estrellas visuales.
    """
    if not rating:
        return "Sin calificación"
    full_stars = int(rating // 2)
    empty_stars = 5 - full_stars
    return "★" * full_stars + "☆" * empty_stars

@register.filter
def format_date_es(date):
    """
    Convierte una fecha al formato "26 de Mayo de 1976".
    """
    if not date:
        return "Fecha no disponible"
    months_es = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    return f"{date.day} de {months_es[date.month - 1]} de {date.year}"
