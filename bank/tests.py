from django.test import TestCase

from bank.exceptions import CurrencyExchangeRateNotAvailable
from bank.models import CurrencyRate
from bank.utils.currency import convert, get_currency_display


class CurrencyUtilsTests(TestCase):

    def setUp(self) -> None:
        CurrencyRate.objects.bulk_create([
            CurrencyRate(currency='EUR', rate=25),
            CurrencyRate(currency='USD', rate=10),
        ])

    def test_currency_conversion__from_to_same(self):
        self.assertEqual(convert(100, 'EUR', 'EUR'), 100)

    def test_currency_conversion__international_to_domestic(self):
        self.assertEqual(convert(100, 'EUR', 'CZK'), 2500)

    def test_currency_conversion__domestic_to_international(self):
        self.assertEqual(convert(100, 'CZK', 'EUR'), 4)

    def test_currency_conversion__international_to_international(self):
        self.assertEqual(convert(100, 'EUR', 'USD'), 250)

    def test_currency_conversion__invalid_currency(self):
        with self.assertRaises(CurrencyExchangeRateNotAvailable):
            convert(100, 'EUR', 'ABC')

    def test_currency_display(self):
        self.assertEqual(get_currency_display('CZK'), 'koruna (CZK)')
