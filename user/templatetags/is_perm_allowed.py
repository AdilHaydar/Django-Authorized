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