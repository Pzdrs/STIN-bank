from babel.numbers import format_currency
from django.test import TestCase

from bank.utils.currency import CURRENCIES


# Create your tests here.

def test_currency_format():
    for currency in CURRENCIES.keys():
        balance = format_currency(
            10000, currency, format=u"#,##0.00 ¤", locale="cs_CZ"
        ).split(',')
        print(balance)