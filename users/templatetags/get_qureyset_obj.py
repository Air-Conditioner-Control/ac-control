from django.template.defaulttags import register
from django import template

register = template.Library()


@register.filter
def get_qureyset_obj(dictionary, key):
    return getattr(dictionary, key)