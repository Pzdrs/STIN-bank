import pyotp
from decouple import config
from django.contrib.auth.models import AbstractUser
from django.db import models

from STINBank.utils.config import get_bank_config
from bank.utils.currency import CURRENCIES__MODELS, get_currency_display


class User(AbstractUser):
    preferred_currency = models.CharField(max_length=3, choices=CURRENCIES__MODELS, null=True, blank=True)
    use_2fa = models.BooleanField(default=False)
    pending_verification = models.BooleanField(default=False)

    def get_preferred_currency_display(self):
        return get_currency_display(self.preferred_currency)

    def has_preferred_currency(self):
        return self.preferred_currency is not None

    def get_full_name_reversed(self):
        return f'{self.last_name} {self.first_name}'.strip()

    def has_pending_verification(self):
        return self.pending_verification

    def is_using_2fa(self):
        return self.use_2fa

    def set_pending_verification(self, state: bool):
        self.pending_verification = state
        self.save()

    def get_totp_uri(self):
        return pyotp.totp.TOTP(config('TOTP_KEY')).provisioning_uri(
            name=self.username,
            issuer_name=get_bank_config().name
        )
