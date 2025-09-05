from django import template

register = template.Library()

@register.filter
def keyvalue(d, key):
    return d.get(key, "")  # safely returns empty string if key not found
