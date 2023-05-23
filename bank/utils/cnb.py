import requests
from django.core.exceptions import ObjectDoesNotExist

from STINBank.utils.config import get_bank_config
from bank.models import CurrencyRate


class Currency:
    def __init__(self, country: str, currency: str, amount: int, code: str, rate: float):
        self.country = country
        self.currency = currency
        self.amount = amount
        self.code = code
        self.rate = rate

    def __str__(self) -> str:
        return f'{self.currency} ({self.code})'


def fetch_rates() -> tuple[Currency]:
    data = requests.get(get_bank_config().cnb_rates_url)
    rates = []
    for line in data.text.split('\n')[2:-1]:
        # země|měna|množství|kód|kurz
        data = line.split('|')
        rates.append(Currency(data[0], data[1], int(data[2]), data[3], float(data[4].replace(',', '.'))))
    return tuple(rates)


def update_rates(debug: bool = False):
    for currency_data in fetch_rates():
        changes_made = False
        if debug:
            print(f'Processing {currency_data}')
        try:
            currency_rate = CurrencyRate.objects.get(currency=currency_data.code)
            if currency_rate.rate != currency_data.rate:
                if debug:
                    print(f'Updating {currency_data.code} from {currency_rate.rate} to {currency_data.rate}...', end='')
                currency_rate.rate = currency_data.rate
                changes_made = True
        except ObjectDoesNotExist:
            if debug:
                print(f'Creating a new CurrencyRate object for {currency_data} with the value {currency_data.rate}...')
            currency_rate = CurrencyRate(currency=currency_data.code, rate=currency_data.rate/currency_data.amount)
            changes_made = True
        currency_rate.save()
        if debug:
            print('done' if changes_made else 'Currency up-to-date')
