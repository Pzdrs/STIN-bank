import random
import string

from django.contrib.auth.models import User
from django.db import models


class AccountQuerySet(models.QuerySet):
    def for_user(self, user: User):
        return self.filter(owner=user)

    def for_number(self, number: str):
        return self.filter(account_number=number)


def generate_account_number():
    while True:
        random_number = random.choices(string.digits, k=13)
        if not Account.objects.for_number(random_number):
            return f'{"".join(random_number[:3])}-{"".join(random_number[3:])}'


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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.account_number = generate_account_number()
        super().save(force_insert, force_update, using, update_fields)

    def get_balance(self, currency: str = None):
        account_balance = AccountBalance.objects.for_account(self)
        if currency:
            account_balance = account_balance.filter(currency=currency)
        return account_balance

    @property
    def display_name(self):
        return self.name if self.name else self.get_type_display()


class Currency:
    def __init__(self, country: str, currency: str, amount: int, code: str, rate: float):
        self.country = country
        self.currency = currency
        self.amount = amount
        self.code = code
        self.rate = rate


class AccountBalanceQuerySet(models.QuerySet):
    def for_account(self, account: Account):
        return self.filter(account=account)


class AccountBalance(models.Model):
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
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    # ISO 4217 currency code
    currency = models.CharField(max_length=3, choices=CURRENCIES, default=CURRENCIES[0])
    balance = models.FloatField(default=0)

    objects = AccountBalanceQuerySet.as_manager()
