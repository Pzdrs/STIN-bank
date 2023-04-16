from django import forms

from bank.models import Account
from bank.utils.currency import CURRENCIES__MODELS, CURRENCIES


class TransactionForm(forms.Form):
    origin_account_pk = forms.IntegerField(
        label='',
        widget=forms.HiddenInput()
    )
    target_account_number = forms.CharField(
        label='Číslo cílového účtu', max_length=24,
        widget=forms.TextInput(attrs={'class': 'input'})
    )
    currency = forms.ChoiceField(label='Měna', choices=CURRENCIES__MODELS)
    amount = forms.DecimalField(
        label='Částka', max_digits=12, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'input'})
    )

    origin_account: Account = None
    target_account: Account = None

    def __init__(self, account: Account, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if account:
            self.fields['origin_account_pk'].initial = account.pk
            self.fields['currency'].choices = (
                (bal.currency, CURRENCIES[bal.currency]) for bal in account.get_currency_balances()
            )
            # TODO: set initial currency to the one set as default in the account
            # self.fields['currency'].initial = smtn

    def clean(self):
        cleaned_data = super().clean()

        try:
            self.origin_account = Account.objects.get(pk=cleaned_data['origin_account_pk'])
            self.target_account = Account.objects.get(account_number=cleaned_data['target_account_number'])
        except Account.DoesNotExist:
            raise forms.ValidationError('Cílový účet neexistuje.')

        return cleaned_data
