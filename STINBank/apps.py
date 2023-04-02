from django.apps import AppConfig
from django.urls import reverse_lazy


class STINBankConfig(AppConfig):
    name = 'STINBank'
    default_title = 'STIN Bank'
    default_page = reverse_lazy('bank:dashboard')
