from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = 'Creates a demo user.'

    def handle(self, *args, **kwargs):
        admin: User = User(
            username='administrator', email='admin@stb.cz', first_name='Roman', last_name='Špánek',
            is_staff=True, is_superuser=True
        )
        admin.set_password('admin')
        admin.save()
        print(f'Created demo user: {admin.username}')
