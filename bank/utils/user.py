from django.contrib.auth.models import User

from STINBank.utils.config import get_bank_config
from bank.models import UserPreferredCurrency


def get_user_preferred_currency(user: User) -> str:
    preferred_currency = UserPreferredCurrency.objects.for_user(user)
    if not preferred_currency:
        return get_bank_config().default_currency
    return preferred_currency.currency
