from django import template

register = template.Library()

@register.filter
def make_range(value):
    return range(value)
