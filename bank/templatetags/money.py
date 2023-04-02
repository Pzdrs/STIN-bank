from babel.numbers import format_currency
from django import template

from bank.utils.user import get_user_preferred_currency

register = template.Library()


@register.inclusion_tag('includes/account_balance.html', takes_context=True)
def account_balance(context, account):
    currency = get_user_preferred_currency(context.request.user)
    balance = format_currency(
        account.get_total_balance(currency), currency, format=u"#,##0.00 ¤", locale="cs_CZ"
    ).split(',')
    return {
        'balance_whole': balance[0],
        'balance_decimal': balance[1]
    }
