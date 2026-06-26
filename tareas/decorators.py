from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def roles_permitidos(*roles):
    
    def decorator(view_func):
        
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            
            if not request.user.is_authenticated:
                return redirect('login')
            
            grupos = request.user.groups.values_list('name', flat=True)
            
            if any(grupo in roles for grupo in grupos):
                return view_func(request, *args, **kwargs)
            
            print("NO TIENE PERMISOS")
            messages.error(request, "No tienes permisos para acceder a esta página. ")
            return redirect("dashboard")
        
        return wrapper
    
    return decorator