from django import template
from datetime import datetime

register = template.Library()

@register.filter
def mostra_tempo(val1, val2):
    if isinstance(val1, datetime) and isinstance(val2, datetime):
        dias = (val1 - val2).days
        if dias > 1:
            return f'{(val1 - val2).days} Dias.'
        return f'{(val1 - val2).days} Dia.'


    return "Ainda não foi devolvido"