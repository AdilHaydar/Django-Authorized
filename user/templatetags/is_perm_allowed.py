from django import template


register = template.Library()

@register.filter(name='isAuth')
def isAuth(user,process):
    if user.group:
        user_perms = user.group.permissions.values_list('codename',flat=True)
        if process in user_perms:
            return True
    
    else:
        return False

@register.filter(name='is_selected')
def is_selected(foo,bar):
    foo = str(foo)
    bar = str(bar)

    if foo==bar:
        return True
    return False

@register.filter(name='is_authorized')
def is_authorized(user,perm):
    if user.is_superuser:
        return True
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
