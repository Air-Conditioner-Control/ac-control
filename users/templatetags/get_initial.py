from django.template.defaulttags import register
from django import template

register = template.Library()


@register.filter
def get_initial(name):

    name = str(name)
    if name:
        name = name.split(' ')
        if len(name) > 1:
            result = name[0][0] + name[1][0]
        else:
            result = name[0][0] + name[0][1]
    else:
        result = '  '
    return result