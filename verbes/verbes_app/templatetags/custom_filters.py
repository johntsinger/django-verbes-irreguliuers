from django import template

register = template.Library()

@register.filter
def index(list_item, i):
    """Template filter to filtring list by index"""
    try:
        return list_item[i]
    except:
        return None

@register.filter
def count_done(item):
    return item.filter(done=True).count()

@register.filter
def count_success(item):
    return item.filter(success=True).count()

@register.filter
def count_remainders(item):
    return item.all().count() - count_done(item)