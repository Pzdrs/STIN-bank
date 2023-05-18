from STINBank.celery import app
from bank.utils.cnb import update_rates


@app.task
def update_rates_task():
    update_rates()
