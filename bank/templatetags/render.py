from babel.numbers import format_currency
from django import template
from django.http import HttpRequest

from accounts.models import User
from bank.models import Transaction, Account

register = template.Library()


@register.inclusion_tag('includes/transaction_table_row.html')
def render_transaction_table_row(transaction: Transaction, account: Account, request: HttpRequest):
    return {
        'transaction': transaction,
        'account': account,
        'is_incoming_transaction': transaction.is_incoming(account),
        'is_outgoing_transaction': transaction.is_outgoing(account),
    }


@register.inclusion_tag('includes/account_balance.html')
def render_account_balance(account: Account, request: HttpRequest, size: int):
    user: User = request.user
    currency = user.get_preferred_currency()
    return render_monetary_value(account.get_total_balance(currency), currency, size)


@register.inclusion_tag('includes/account_balance.html')
def render_monetary_value(value: float, currency: str, size: int):
    balance = format_currency(
        value, currency, format=u"#,##0.00 ¤", locale="cs_CZ"
    )
    split_balance = balance.split(',' if ',' in balance else ' ')
    balance_whole = split_balance[0]
    balance_decimal = ('00 ' if ',' not in balance else '') + split_balance[1]

    return {
        'whole_part': balance_whole,
        'decimal_part': balance_decimal,
        'size': size
    }
