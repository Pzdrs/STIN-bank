from django.contrib import admin

from bank.models import Account, AccountBalance


# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(AccountBalance)
class AccountBalanceAdmin(admin.ModelAdmin):
    pass
