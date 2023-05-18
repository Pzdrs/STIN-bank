from django.core.management.base import BaseCommand

from bank.utils.cnb import update_rates


class Command(BaseCommand):
    help = 'Fetches the exchange rates from CNB and updates the database'

    def handle(self, *args, **kwargs):
        update_rates(debug=True)
