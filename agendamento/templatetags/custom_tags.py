from django import template
from agendamento.models import *
from django.db.models import Q, Avg

register = template.Library()

@register.filter(name='avg_rating')
def avg_rating(value,arg):
    if value.commentcliente_set.aggregate(Avg('rating'))['rating__avg'] == None:
        return 5
    return value.commentcliente_set.aggregate(Avg('rating'))['rating__avg']
