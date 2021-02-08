from django import template


register = template.Library()

@register.filter(name='is_authorized')
def is_authorized(user,perm):
    if user.group:
        user_perms = user.group.permissions.values_list('codename',flat=True)
        if perm in user_perms:
            return True
    else:
        return False
    
@register.filter(name='dropdown_filter')
def dropdown_filter(user,perms):
    if user.is_superuser:
        return True
    perms = set(perms.split(' '))
    user_perms = set(user.group.permissions.values_list('codename',flat=True))
    if len(perms.intersection(user_perms)) != 0:
        return True
    
    return False
