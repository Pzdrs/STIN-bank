from django.core.exceptions import ObjectDoesNotExist

from STINBank.celery import app
from bank.models import CurrencyRate
from bank.utils.cnb import fetch_rates


@app.task
def update_rates():
    for currency_data in fetch_rates():
        try:
            currency_rate = CurrencyRate.objects.get(currency=currency_data.code)
            currency_rate.rate = currency_data.rate
        except ObjectDoesNotExist:
            currency_rate = CurrencyRate(currency=currency_data.code, rate=currency_data.rate)
        currency_rate.save()
