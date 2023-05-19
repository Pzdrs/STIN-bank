import random
import string

from babel.numbers import format_currency
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models import Q
from django.http import HttpRequest

from STINBank.utils.config import get_bank_config
from bank.utils.currency import get_default_currency, CURRENCIES__MODELS, convert


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


class Account(models.Model):
    class AccountType(models.TextChoices):
        MUJUCET = 'mujucet', 'MůjÚčet'
        MUJUCET_PLUS = 'mujucet_plus', 'MůjÚčet PLUS'
        MUJUCET_GOLD = 'mujucet_gold', 'MůjÚčet GOLD'
        G2 = 'g2', 'Studentský účet G2'

    account_number = models.CharField(max_length=14, editable=False, unique=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    type = models.CharField(max_length=15, choices=AccountType.choices, default=AccountType.MUJUCET)
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

    def get_balances(self):
        """
        Returns an AccountBalanceQuerySet with all the balances associated with this account
        """
        return AccountBalance.objects.for_account(self)

    def get_balance(self, currency: str):
        """
        Returns an AccountBalanceQuerySet with all the balances in a given currency associated with this account
        """
        try:
            return AccountBalance.objects.for_account(self).get(currency=currency)
        except ObjectDoesNotExist:
            return None

    def get_default_balance(self):
        """
        :returns: an AccountBalance with the balance in the default currency associated with this account
        """
        return self.get_balances().default(self)

    def get_default_currency(self) -> str:
        return self.get_default_balance().currency

    def get_total_balance(self, currency: str) -> float:
        """
        Returns a value in a given currency that sums up all the balances associated with this account
        """
        total_balance = 0
        for balance in self.get_balances():
            total_balance += balance.convert_to(currency)
        return total_balance

    def add_funds(self, amount: float, currency: str, convert_over_create: bool = False):
        """
        Adds funds to the default currency balance of this account
        The default behavior is to create a new balance in the specified currency, if it doesn't exist
        If convert_over_create is set to True, the funds will be converted and added to the default balance (in that currency)
        """
        amount = abs(amount)
        currency_balance: AccountBalance = self.get_balance(currency)
        if currency_balance:
            currency_balance.add_funds(amount)
        else:
            if convert_over_create:
                default_balance = self.get_default_balance()
                default_balance.add_funds(
                    convert(amount, currency, default_balance.currency)
                )
            else:
                AccountBalance.objects.create(account=self, currency=currency, balance=amount)

    def subtract_funds(self, amount: float, currency: str, transfer: bool = False):
        """
        Subtracts funds from the default currency balance of this account
        """
        currency_balance: AccountBalance = self.get_balance(currency)

        if currency_balance:
            if currency_balance.balance >= amount:
                currency_balance.subtract_funds(amount)
            else:
                raise Transaction.InsufficientFunds(currency)
        else:
            if transfer:
                currency_balance = self.get_default_balance()
                currency_balance.subtract_funds(
                    convert(amount, currency, currency_balance.currency)
                )
            else:
                raise Transaction.InsufficientFunds(currency)

    @property
    def get_account_number(self):
        return f'{self.account_number}/0000'

    @property
    def display_name(self):
        return self.name if self.name else self.get_type_display()

    @property
    def assets_overview(self):
        def get_word_version(count: int):
            word_versions = ('měna', 'měny', 'měn')
            if count == 1:
                return word_versions[0]
            elif 1 < count < 5:
                return word_versions[1]
            else:
                return word_versions[2]

        balance_count = self.get_balances().count()
        if balance_count == 0:
            return ''
        return f'({balance_count} {get_word_version(balance_count)})'

    def get_transactions(self):
        return Transaction.objects.for_account(self)

    def get_outgoing_transactions(self):
        return Transaction.objects.outgoing(self)

    def get_incoming_transactions(self):
        return Transaction.objects.incoming(self)


class AccountBalanceQuerySet(models.QuerySet):
    def for_account(self, account: Account) -> 'AccountBalanceQuerySet':
        return self.filter(account=account)

    def default(self, account: Account) -> 'AccountBalance':
        try:
            return self.for_account(account).get(default_balance=True)
        except ObjectDoesNotExist:
            return AccountBalance.objects.create(
                account=account, currency=get_bank_config().default_currency
            )


class AccountBalance(models.Model):
    class Meta:
        unique_together = ('account', 'currency')
        constraints = [
            models.UniqueConstraint(
                fields=['account', 'default_balance'],
                condition=models.Q(default_balance=True),
                name='unique_default_balance'
            ),
        ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    # ISO 4217 currency code
    currency = models.CharField(max_length=3, choices=CURRENCIES__MODELS, default=get_default_currency())
    balance = models.FloatField(default=0)
    default_balance = models.BooleanField(default=False)

    objects = AccountBalanceQuerySet.as_manager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # If this is the first balance for the account, set it as default
        if self.account.get_balances().count() == 0:
            self.default_balance = True
        super().save(force_insert, force_update, using, update_fields)

    def set_default(self):
        self.account.get_balances().update(default_balance=False)
        self.default_balance = True
        self.save()

    def add_funds(self, amount: float):
        self.balance += amount
        self.save()

    def subtract_funds(self, amount: float):
        self.add_funds(-amount)

    def convert_to(self, currency: str) -> float:
        return convert(self.balance, self.currency, currency)

    @property
    def balance_display(self):
        return format_currency(
            self.balance, self.currency, format=u"#,##0.00 ¤", locale="cs_CZ"
        )

    def __str__(self):
        return f'{self.balance} {self.currency}'


class CurrencyRate(models.Model):
    currency = models.CharField(max_length=3, choices=CURRENCIES__MODELS, unique=True)
    rate = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)


class TransactionQuerySet(models.QuerySet):
    def create_non_transfer(
            self,
            account: Account,
            transaction_type: 'Transaction.TransactionType',
            amount: float, currency: str,
            request: HttpRequest = None
    ):
        transaction = Transaction(type=transaction_type, currency=currency, amount=amount)
        match transaction_type:
            case Transaction.TransactionType.DEPOSIT:
                transaction.target = account
            case Transaction.TransactionType.WITHDRAWAL:
                transaction.origin = account

        # Attempt to authorize the transaction, handle all exceptions
        try:
            transaction.authorize()
        except (Transaction.InsufficientFunds, Transaction.InvalidTransactionType) as e:
            if request:
                messages.error(request, str(e))
            else:
                raise e
            return

        # If the transaction was authorized and the request was passed, display a success message
        if request:
            if transaction_type == Transaction.TransactionType.DEPOSIT:
                messages.success(request, 'Peníze byly úspěšně připsány na účet.')
            elif transaction_type == Transaction.TransactionType.WITHDRAWAL:
                messages.success(request, 'Peníze byly úspěšně vybrány z účtu.')

    def for_account(self, account: Account):
        return self.filter(Q(origin=account) | Q(target=account))

    def outgoing(self, account: Account):
        return self.filter(origin=account)

    def incoming(self, account: Account):
        return self.filter(target=account)


class Transaction(models.Model):
    class InsufficientFunds(Exception):

        def __init__(self, currency: str) -> None:
            super().__init__(f'Pro tuto transakci v měně {currency} nemáte dostatek prostředků.')

    class InvalidTransactionType(Exception):

        def __init__(self, transaction_type: str) -> None:
            super().__init__(f'Transakce typu {transaction_type} není podporována.')

    class TransactionType(models.TextChoices):
        TRANSFER = 'TRANSFER', 'Převod'
        DEPOSIT = 'DEPOSIT', 'Vklad'
        WITHDRAWAL = 'WITHDRAWAL', 'Výběr'

    type = models.CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.TRANSFER)
    origin = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='origin_accounts', null=True, blank=True)
    target = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='target_accounts', null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCIES__MODELS, default=get_default_currency())
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TransactionQuerySet.as_manager()

    def clean(self):
        if self.origin == self.target:
            raise ValidationError('Origin and target accounts cannot be the same.')
        # if transaction is transfer, both origin and target must be set
        if self.type == self.TransactionType.TRANSFER and (not self.origin or not self.target):
            raise ValidationError('Origin and target must be set for a transfer transaction.')
        # if transaction is deposit, only target must be set
        if self.type == self.TransactionType.DEPOSIT and (self.origin or not self.target):
            raise ValidationError('Target must be set for a deposit.')
        # if transaction is withdrawal, only origin must be set
        if self.type == self.TransactionType.WITHDRAWAL and (not self.origin or self.target):
            raise ValidationError('Origin must be set for a withdrawal.')

    def is_incoming(self, account: Account):
        if self.type != self.TransactionType.TRANSFER:
            return False
        return self.target == account

    def is_outgoing(self, account: Account):
        if self.type != self.TransactionType.TRANSFER:
            return False
        return self.origin == account

    def get_direction(self, account: Account):
        """
        :returns: 1 if the transaction is incoming (inflow of funds), -1 if the transaction is
        outgoing (outflow of funds), 0 if the transaction is not related to the account
        """
        if self.type == self.TransactionType.TRANSFER:
            if self.origin == account:
                return -1
            if self.target == account:
                return 1
        if self.type == self.TransactionType.DEPOSIT:
            return 1
        if self.type == self.TransactionType.WITHDRAWAL:
            return -1
        return 0

    def authorize(self):
        match self.type:
            case self.TransactionType.TRANSFER:
                self.origin.subtract_funds(self.amount, self.currency, True)
                self.target.add_funds(self.amount, self.currency, convert_over_create=True)
            case self.TransactionType.DEPOSIT:
                self.target.add_funds(self.amount, self.currency)
            case self.TransactionType.WITHDRAWAL:
                self.origin.subtract_funds(self.amount, self.currency)
            case _:
                raise Transaction.InvalidTransactionType(self.type)
        self.save()

    def __str__(self):
        return f'{self.type} - {self.amount} {self.currency} | {self.origin} -> {self.target}'
