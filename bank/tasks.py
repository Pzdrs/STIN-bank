from django.contrib import messages
from django.http import HttpRequest

from STINBank.celery import app
from bank.models import Account
from bank.utils.cnb import update_rates


@app.task
def update_rates_task():
    update_rates()


@app.task
def authorize_transaction(request: HttpRequest, origin: Account, target: Account, amount: float, currency: str):
    print(f'Authorizing transaction from {origin} to {target} of {amount} {currency}')
    messages.success(request, 'Transakce byla úspěšně provedena.')
