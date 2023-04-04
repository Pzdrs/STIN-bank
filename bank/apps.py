from django.apps import AppConfig


class BankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bank'
    cnb_rates_url = 'https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt'
    default_currency = 'CZK'
    # Used as a middle man for currency exchanges
    base_currency = 'CZK'
    # TODO
    # -1 for unlimited
    max_accounts = 5
