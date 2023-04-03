from django.contrib.auth.models import AbstractUser
from django.db import models

from STINBank.utils.config import get_bank_config
from bank.utils.constants import CURRENCIES


class User(AbstractUser):
    preferred_currency = models.CharField(max_length=3, choices=CURRENCIES, null=True, blank=True)

    def get_preferred_currency(self):
        return self.preferred_currency if self.preferred_currency else get_bank_config().default_currency
