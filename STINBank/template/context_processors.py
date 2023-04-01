from django.http import HttpRequest

from STINBank.utils.config import get_project_config


def defaults(request: HttpRequest):
    return {
        'defaults': {
            'title': get_project_config().default_title,
        }
    }
