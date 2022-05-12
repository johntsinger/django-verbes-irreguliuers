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
def replace(item, characters):
    """Add a space of each side of a given character if it is in the item"""
    if characters in item:
        return item.replace(characters, " " + characters + " ")
    return item

@register.filter
def count_done(item):
    """Count the number of item that have the done=True attribute"""
    return item.filter(done=True).count()

@register.filter
def count_success(item):
    """Count the number of item that have the success=True attribute"""
    return item.filter(success=True).count()

@register.filter
def count_remainders(item):
    """Count the number of item that are not done"""
    return item.all().count() - count_done(item)