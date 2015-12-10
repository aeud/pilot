from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.simple_tag()
def auto_td(val):
    if re.search('^\-?\d+(,\d{3})*(\.\d+)?\%$', str(val)):
        if re.search('^\-', str(val)):
            html = '<span class="' + 'positive pourcent' + '">' + str(val) + '</span>'
        else:
            html = '<span class="' + 'negative pourcent' + '">' + str(val) + '</span>'
    else:
        html = val
    return mark_safe(html)