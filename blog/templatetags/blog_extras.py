from django import template
import math

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    min_value = 5
    multiplied = math.floor(value * arg)
    if min_value > multiplied:
        return min_value
    else:
        return multiplied