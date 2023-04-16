from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, CreateView, FormView

from STINBank.utils.config import get_bank_config
from STINBank.utils.template import push_form_errors_to_messages
from STINBank.views import BankView
from bank.forms import TransactionForm
from bank.models import Account, Transaction, AccountBalance
from bank.tasks import authorize_transaction


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
    paginate_by = get_bank_config().transaction_history_paginate_by

    account: Account = None

    def get(self, request, *args, **kwargs):
        self.account = Account.objects.get(pk=self.kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['account'] = self.account

        return context

    def get_queryset(self):
        return self.account.get_transactions().order_by('-created_at')


class AccountTransactionView(BankView, FormView):
    template_name = 'transaction.html'
    form_class = TransactionForm
    title = 'Transakce'
    success_url = reverse_lazy('bank:dashboard')
    account: Account = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['account'] = self.account
        return kwargs

    def get(self, request, *args, **kwargs):
        self.account = Account.objects.get(pk=self.kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        push_form_errors_to_messages(self.request, form)
        return super().form_invalid(form)

    def form_valid(self, form):
        authorize_transaction(
            self.request,
            form.origin_account, form.target_account,
            form.cleaned_data['currency'], form.cleaned_data['amount']
        )
        return super().form_valid(form)


class ChangeDefaultCurrencyBalance(BankView, View):
    def post(self, request, *args, **kwargs):
        account: Account = Account.objects.get(pk=self.kwargs['pk'])
        current_default_balance: AccountBalance = account.get_default_balance()
        new_default_balance: AccountBalance = account.get_currency_balance(request.POST['currency'])
        new_default_balance.set_default()
        messages.success(
            request,
            f'Výchozí měna účtu byla změněna z {current_default_balance.currency} na {new_default_balance.currency}.'
        )
        return HttpResponseRedirect(reverse('bank:account-detail', kwargs={'pk': account.pk}))
