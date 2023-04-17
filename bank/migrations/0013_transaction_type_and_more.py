# Generated by Django 4.2 on 2023-04-17 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0012_accountbalance_default_balance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('TRANSFER', 'Převod'), ('DEPOSIT', 'Vklad'), ('WITHDRAWAL', 'Výběr')], default='TRANSFER', max_length=10),
        ),
        migrations.AlterField(
            model_name='accountbalance',
            name='default_balance',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='origin_accounts', to='bank.account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='target',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_accounts', to='bank.account'),
        ),
    ]
