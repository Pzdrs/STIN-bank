from django.forms import ModelForm

from accounts.models import User


class PreferredCurrencyForm(ModelForm):
    class Meta:
        model = User
        fields = ('preferred_currency',)
