from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect()
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_groups(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            group = None
            if request.user.group:
                group = request.user.group.name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

def allowed_perms(allowed_perm):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            

            if allowed_perm in request.user.group.permissions.values_list('codename',flat=True):

                return view_func(request, *args, **kwargs)

            return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator
