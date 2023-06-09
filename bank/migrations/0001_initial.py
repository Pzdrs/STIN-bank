# Generated by Django 4.1.7 on 2023-03-31 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccountBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('AUD', 'dolar'), ('BRL', 'real'), ('BGN', 'lev'), ('CNY', 'žen-min-pi'), ('DKK', 'koruna'), ('EUR', 'euro'), ('PHP', 'peso'), ('HKD', 'dolar'), ('INR', 'rupie'), ('IDR', 'rupie'), ('ISK', 'koruna'), ('ILS', 'nový šekel'), ('JPY', 'jen'), ('ZAR', 'rand'), ('CAD', 'dolar'), ('KRW', 'won'), ('HUF', 'forint'), ('MYR', 'ringgit'), ('MXN', 'peso'), ('XDR', 'ZPČ'), ('NOK', 'koruna'), ('NZD', 'dolar'), ('PLN', 'zlotý'), ('RON', 'leu'), ('SGD', 'dolar'), ('SEK', 'koruna'), ('CHF', 'frank'), ('THB', 'baht'), ('TRY', 'lira'), ('USD', 'dolar'), ('GBP', 'libra')], max_length=3)),
                ('balance', models.FloatField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.account')),
            ],
        ),
    ]
