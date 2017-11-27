from django import template
from django.utils.safestring import mark_safe
import math

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    min_value = 5
    max_value = 72
    multiplied = math.floor(value * arg)
    if min_value > multiplied:
        return min_value
    elif multiplied > max_value:
    	return max_value
    else:
        return multiplied

@register.filter(name='nbsp')
def nbsp(value):
	return mark_safe("&nbsp;".join(value.split(' ')))