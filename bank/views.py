from django.views.generic import TemplateView, DetailView

from STINBank.views import BankView
from bank.models import Account


# Create your views here.

class DashboardView(BankView, TemplateView):
    template_name = 'dashboard.html'
    title = 'Dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['accounts'] = Account.objects.for_user(self.request.user)
        Account.objects.first().get_outgoing_transactions()

        return context


class AccountDetailView(BankView, DetailView):
    template_name = 'account_detail.html'
    model = Account

    def get_title(self):
        return self.object.display_name


