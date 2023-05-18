from django.core.management.base import BaseCommand

from accounts.models import User
from bank.models import Account


class Command(BaseCommand):
    help = 'Creates demo accounts.'

    def handle(self, *args, **kwargs):
        admin: User = User.objects.get(pk=1)
        Account(owner=admin, type=Account.AccountType.MUJUCET, name='Demo účet 1').save()
        Account(owner=admin, type=Account.AccountType.G2, name='Demo účet 2').save()
        print('Created demo accounts.')
