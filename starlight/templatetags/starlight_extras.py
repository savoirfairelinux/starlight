from django import template

from starlight.models import Employee

register = template.Library()


@register.filter(name='search')
def search(wanted_value, list_values):
    return any(element.skill == wanted_value for element in list_values)


register.filter('search', search)
