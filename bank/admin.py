from django.contrib import admin

from bank.models import Account, AccountBalance, CurrencyRate, Transaction


# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('get_account_name', 'type', 'owner')

    @admin.display(description='Account name')
    def get_account_name(self, obj: Account):
        return obj.name if obj.name else '-'


@admin.register(AccountBalance)
class AccountBalanceAdmin(admin.ModelAdmin):
    list_display = ('account', 'currency', 'balance', 'default_balance')


@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'rate', 'updated_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'origin', 'target', 'currency', 'amount')
