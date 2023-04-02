import random
import string

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

CURRENCIES = (
    ('CZK', 'koruna (CZK)'), ('AUD', 'dolar (AUD)'), ('BRL', 'real (BRL)'), ('BGN', 'lev (BGN)'),
    ('CNY', 'žen-min-pi (CNY)'), ('DKK', 'koruna (DKK)'), ('EUR', 'euro (EUR)'), ('PHP', 'peso (PHP)'),
    ('HKD', 'dolar (HKD)'), ('INR', 'rupie (INR)'), ('IDR', 'rupie (IDR)'), ('ISK', 'koruna (ISK)'),
    ('ILS', 'nový šekel (ILS)'), ('JPY', 'jen (JPY)'), ('ZAR', 'rand (ZAR)'), ('CAD', 'dolar (CAD)'),
    ('KRW', 'won (KRW)'), ('HUF', 'forint (HUF)'), ('MYR', 'ringgit (MYR)'), ('MXN', 'peso (MXN)'),
    ('XDR', 'ZPČ (XDR)'), ('NOK', 'koruna (NOK)'), ('NZD', 'dolar (NZD)'), ('PLN', 'zlotý (PLN)'),
    ('RON', 'leu (RON)'), ('SGD', 'dolar (SGD)'), ('SEK', 'koruna (SEK)'), ('CHF', 'frank (CHF)'),
    ('THB', 'baht (THB)'), ('TRY', 'lira (TRY)'), ('USD', 'dolar (USD)'), ('GBP', 'libra (GBP)')
)


def generate_account_number():
    while True:
        random_number = random.choices(string.digits, k=13)
        if not Account.objects.for_number(random_number):
            return f'{"".join(random_number[:3])}-{"".join(random_number[3:])}'


class AccountQuerySet(models.QuerySet):
    def for_user(self, user: User):
        return self.filter(owner=user)

    def for_number(self, number: str):
        return self.filter(account_number=number)


class UserPreferredCurrencyQuerySet(models.QuerySet):
    def for_user(self, user: User):
        try:
            return self.get(user=user)
        except ObjectDoesNotExist:
            return None


class UserPreferredCurrency(models.Model):
    class Meta:
        verbose_name_plural = 'User preferred currencies'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCIES)

    objects = UserPreferredCurrencyQuerySet.as_manager()


class Account(models.Model):
    ACCOUNT_TYPES = (
        ('mujucet', 'MůjÚčet'),
        ('mujucet_plus', 'MůjÚčet PLUS'),
        ('mujucet_gold', 'MůjÚčet GOLD'),
        ('g2', 'Studentský účet G2'),
    )
    account_number = models.CharField(max_length=14, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=15, choices=ACCOUNT_TYPES, default=ACCOUNT_TYPES[0])
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountQuerySet.as_manager()

    def __str__(self):
        return f'{self.account_number} - {self.display_name}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self._state.adding:
            self.account_number = generate_account_number()
        super().save(force_insert, force_update, using, update_fields)

    def get_currency_balances(self):
        """
        Returns an AccountBalanceQuerySet with all the balances associated with this account
        """
        return AccountBalance.objects.for_account(self)

    def get_currency_balance(self, currency: str):
        """
        Returns an AccountBalanceQuerySet with all the balances in a given currency associated with this account
        """
        return AccountBalance.objects.for_account(self).filter(currency=currency)

    # TODO
    def get_total_balance(self, currency: str) -> float:
        """
        Returns a value in a given currency that sums up all the balances associated with this account
        """
        total_balance = 0
        for balance in self.get_currency_balances():
            pass
        return total_balance

    @property
    def display_name(self):
        return self.name if self.name else self.get_type_display()


class AccountBalanceQuerySet(models.QuerySet):
    def for_account(self, account: Account):
        return self.filter(account=account)


class AccountBalance(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    # ISO 4217 currency code
    currency = models.CharField(max_length=3, choices=CURRENCIES, default=CURRENCIES[0])
    balance = models.FloatField(default=0)

    objects = AccountBalanceQuerySet.as_manager()


class CurrencyRate(models.Model):
    currency = models.CharField(max_length=3, choices=CURRENCIES, unique=True)
    rate = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
