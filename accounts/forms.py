from django.forms import ModelForm

from accounts.models import User


class UserForm(ModelForm):
    def __init__(self, data=None, instance=None):
        super().__init__(data, instance=instance)
        for field in self.fields:
            self.fields[field].required = False

    class Meta:
        model = User
        fields = '__all__'


class PreferredCurrencyForm(ModelForm):
    class Meta:
        model = User
        fields = ('preferred_currency',)
