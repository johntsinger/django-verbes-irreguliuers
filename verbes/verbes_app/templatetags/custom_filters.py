from django import template

register = template.Library()

@register.filter
def index(list_item, i):
    """Template filter to filtring list by index"""
    try:
        return list_item[i]
    except:
        return None