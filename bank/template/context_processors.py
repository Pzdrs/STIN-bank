from django.http import HttpRequest

from bank.utils.currency import get_default_currency


def bank_data(request: HttpRequest) -> dict:
    return {
        'default_currency': get_default_currency()
    }
