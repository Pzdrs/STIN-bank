from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = 'Creates demo accounts.'

    def handle(self, *args, **kwargs):
        print('Setting up demo...')
        call_command('create_demo_user')
        call_command('create_demo_accounts')
        print('done')
