from .utils import (
    es_admin,
    es_supervisor,
    es_conductor,
)

def roles(request):
    if request.user.is_authenticated:
        return {
            "es_admin": es_admin(request.user),
            "es_supervisor": es_supervisor(request.user),
            "es_conductor": es_conductor(request.user),
        }

    return {}