from babel.numbers import format_currency
from django import template


register = template.Library()


@register.inclusion_tag('includes/account_balance.html', takes_context=True)
def account_balance(context, account):
    currency = context.request.user.get_preferred_currency()
    balance = format_currency(
        account.get_total_balance(currency), currency, format=u"#,##0.00 ¤", locale="cs_CZ"
    ).split(',')
    return {
        'balance_whole': balance[0],
        'balance_decimal': balance[1]
    }
