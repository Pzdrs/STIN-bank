from django.contrib import messages
from django.http import HttpRequest

from STINBank.celery import app
from bank.models import Account, Transaction
from bank.utils.cnb import update_rates


@app.task
def update_rates_task():
    update_rates()


@app.task
def authorize_transaction(request: HttpRequest, origin: Account, target: Account, currency: str, amount: float):
    transaction = Transaction(
        origin=origin, target=target, currency=currency, amount=amount
    )
    try:
        transaction.authorize()
        messages.success(request, 'Transakce byla úspěšně provedena.')
    except Transaction.InsufficientFunds as e:
        messages.error(request, str(e))
