from django.contrib.auth.models import AbstractUser
from django.db import models

from STINBank.utils.config import get_bank_config
from bank.utils.currency import CURRENCIES__MODELS, get_currency_display


class User(AbstractUser):
    preferred_currency = models.CharField(max_length=3, choices=CURRENCIES__MODELS, null=True, blank=True)
    use_2fa = models.BooleanField(default=False)
    pending_verification = models.BooleanField(default=False)

    def get_preferred_currency(self, default: bool = True):
        """
        Returns the user preferred currency. If the default argument is True, in the case of the user
        not having a preferred currency, the default currency is returned
        """
        if not self.preferred_currency and default:
            return get_bank_config().default_currency
        return self.preferred_currency

    def get_preferred_currency_display(self):
        return get_currency_display(self.get_preferred_currency())

    def has_preferred_currency(self):
        return self.preferred_currency is not None

    def get_full_name_reversed(self):
        return f'{self.last_name} {self.first_name}'

    def has_pending_verification(self):
        return self.pending_verification

    def is_using_2fa(self):
        return self.use_2fa

    def set_pending_verification(self, state: bool):
        self.pending_verification = state
        self.save()
