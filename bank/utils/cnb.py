import requests

from STINBank.utils.config import get_bank_config
from bank.models import Currency


def fetch_rates() -> tuple[Currency]:
    data = requests.get(get_bank_config().cnb_rates_url)
    rates = []
    for line in data.text.split('\n')[2:-1]:
        # země|měna|množství|kód|kurz
        data = line.split('|')
        rates.append(Currency(data[0], data[1], int(data[2]), data[3], float(data[4])))
    return tuple(rates)
