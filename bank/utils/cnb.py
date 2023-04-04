import requests

from STINBank.utils.config import get_bank_config


class Currency:
    def __init__(self, country: str, currency: str, amount: int, code: str, rate: float):
        self.country = country
        self.currency = currency
        self.amount = amount
        self.code = code
        self.rate = rate


def fetch_rates() -> tuple[Currency]:
    data = requests.get(get_bank_config().cnb_rates_url)
    rates = []
    for line in data.text.split('\n')[2:-1]:
        # země|měna|množství|kód|kurz
        data = line.split('|')
        rates.append(Currency(data[0], data[1], int(data[2]), data[3], float(data[4].replace(',', '.'))))
    return tuple(rates)
