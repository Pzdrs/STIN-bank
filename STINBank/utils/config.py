from django.apps import apps

from STINBank.apps import STINBankConfig
from bank.apps import BankConfig


def get_project_config() -> STINBankConfig:
    return apps.get_app_config('STINBank')


def get_bank_config() -> BankConfig:
    return apps.get_app_config('bank')
