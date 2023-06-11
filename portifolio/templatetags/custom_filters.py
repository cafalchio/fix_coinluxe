from django import template
import json

register = template.Library()

@register.filter
def json_value(value):
    return json.dumps(value)