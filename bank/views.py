from django.views.generic import TemplateView, DetailView, ListView

from STINBank.views import BankView
from bank.models import Account, Transaction


# Create your views here.

class DashboardView(BankView, TemplateView):
    template_name = 'dashboard.html'
    title = 'Dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['accounts'] = Account.objects.for_user(self.request.user)

        return context


class AccountDetailView(BankView, DetailView):
    template_name = 'account_detail.html'
    model = Account

    def get_title(self):
        return self.object.display_name


class AccountTransactionHistoryView(BankView, ListView):
    template_name = 'transaction_history.html'
    model = Transaction
    title = 'Historie transakcí'

    account: Account = None

    def get(self, request, *args, **kwargs):
        self.account = Account.objects.get(pk=self.kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['account'] = self.account

        return context

    def get_queryset(self):
        return self.account.get_transactions()
