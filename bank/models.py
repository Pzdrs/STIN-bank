from django.contrib.auth.models import User
from django.db import models


class AccountQuerySet(models.QuerySet):
    def owned_by(self, user: User):
        return self.filter(user=user)


class Account(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountQuerySet.as_manager()

    def get_balance(self, currency: str = None):
        account_balance = AccountBalance.objects.for_account(self)
        if currency:
            account_balance = account_balance.filter(currency=currency)
        return account_balance


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
