# Python Standard Library Imports
from functools import wraps

# Django Imports
from django.http import HttpResponseRedirect


def unauthed_only(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if not (request.user and request.user.is_authenticated):
            return function(request, *args, **kwargs)

        return HttpResponseRedirect(request.GET.get("next", "/"))

    return decorator
