from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = 'Fetches the exchange rates from CNB and updates the database'

    def handle(self, *args, **kwargs):
        admin: User = User(
            username='administrator', email='admin@stb.cz', first_name='Roman', last_name='Špánek',
            is_staff=True, is_superuser=True
        )
        admin.set_password('admin')
