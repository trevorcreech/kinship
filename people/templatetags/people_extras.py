from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(needs_autoescape=True)
@stringfilter
def highlight(value, search_term, autoescape=True, prepend_at_sign=True):
    if prepend_at_sign:
        search_term = "@" + search_term
    return mark_safe(
        value.replace(search_term, "<span class='black fw5'>%s</span>" % search_term)
    )
