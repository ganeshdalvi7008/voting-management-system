from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def voter_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("voter_id"):
            messages.error(request, "Please login as a voter.")
            return redirect("voter_login")
        return view_func(request, *args, **kwargs)
    return wrapper

def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, "Admin access required.")
            return redirect("admin_login")
        return view_func(request, *args, **kwargs)
    return wrapper
