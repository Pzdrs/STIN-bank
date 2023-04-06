from babel.numbers import format_currency
from django import template

register = template.Library()


@register.inclusion_tag('includes/account_balance.html', takes_context=True)
def account_balance(context, account):
    currency = context.request.user.get_preferred_currency()
    balance = format_currency(
        account.get_total_balance(currency), currency, format=u"#,##0.00 ¤", locale="cs_CZ"
    )
    split_balance = balance.split(',' if ',' in balance else ' ')
    balance_whole = split_balance[0]
    balance_decimal = ('00 ' if ',' not in balance else '') + split_balance[1]

    return {
        'balance_whole': balance_whole,
        'balance_decimal': balance_decimal
    }
