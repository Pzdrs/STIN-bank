# Generated by Django 4.2 on 2023-04-03 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='preferred_currency',
            field=models.CharField(blank=True, choices=[('CZK', 'koruna (CZK)'), ('AUD', 'dolar (AUD)'), ('BRL', 'real (BRL)'), ('BGN', 'lev (BGN)'), ('CNY', 'žen-min-pi (CNY)'), ('DKK', 'koruna (DKK)'), ('EUR', 'euro (EUR)'), ('PHP', 'peso (PHP)'), ('HKD', 'dolar (HKD)'), ('INR', 'rupie (INR)'), ('IDR', 'rupie (IDR)'), ('ISK', 'koruna (ISK)'), ('ILS', 'nový šekel (ILS)'), ('JPY', 'jen (JPY)'), ('ZAR', 'rand (ZAR)'), ('CAD', 'dolar (CAD)'), ('KRW', 'won (KRW)'), ('HUF', 'forint (HUF)'), ('MYR', 'ringgit (MYR)'), ('MXN', 'peso (MXN)'), ('XDR', 'ZPČ (XDR)'), ('NOK', 'koruna (NOK)'), ('NZD', 'dolar (NZD)'), ('PLN', 'zlotý (PLN)'), ('RON', 'leu (RON)'), ('SGD', 'dolar (SGD)'), ('SEK', 'koruna (SEK)'), ('CHF', 'frank (CHF)'), ('THB', 'baht (THB)'), ('TRY', 'lira (TRY)'), ('USD', 'dolar (USD)'), ('GBP', 'libra (GBP)')], max_length=3, null=True),
        ),
    ]
