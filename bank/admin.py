from django.contrib import admin

from bank.models import Account, AccountBalance, UserPreferredCurrency, CurrencyRate


# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(AccountBalance)
class AccountBalanceAdmin(admin.ModelAdmin):
    pass


@admin.register(UserPreferredCurrency)
class UserPreferredCurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'rate', 'updated_at')
