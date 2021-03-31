from django import template
from datetime import date
from functools import lru_cache
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='complete_todo')
def complete_todo(todo):
    id = str(todo.id)
    return mark_safe(f'onchange="completeToDo({id})"')


@register.filter(name='delete_todo')
def delete_todo(todo):
    id = todo.id
    return mark_safe(f'onclick="deleteToDo({id})"')


@lru_cache
@register.filter(name='progress')
def date_progress(yeast):
    total = yeast.next_reinnoculation_limit_date - yeast.last_reinnoculation
    passados = yeast.next_reinnoculation_limit_date - date.today()
    progresso = 100 - ((passados.days / total.days)*100)
    if progresso < 0 or progresso >= 100:
        return 100
    else:
        return int(progresso)


@register.filter(name='card')
def card_gradient(yeast):
    progress = date_progress(yeast)
    if progress <= 25:
        return '7'
    elif progress <= 50:
        return '9'
    elif progress <= 75:
        return '3'
    else:
        return '5'


@register.filter(name='icon')
def card_gradient(yeast):
    progress = date_progress(yeast)
    if progress <= 95:
        return 'clock'
    elif progress <= 99:
        return 'exclamation'
    else:
        return 'close'
