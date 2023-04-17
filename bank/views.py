from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, FormView

from STINBank.utils.config import get_bank_config
from STINBank.utils.template import push_form_errors_to_messages
from STINBank.views import BankView
from bank.forms import TransactionForm, AlterFundsForm
from bank.models import Account, Transaction, AccountBalance


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['alter_funds_form'] = AlterFundsForm()

        return context

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
        transaction = Transaction(
            origin=form.origin_account,
            target=form.target_account,
            currency=form.cleaned_data['currency'],
            amount=float(form.cleaned_data['amount'])
        )
        try:
            transaction.authorize()
            messages.success(self.request, 'Transakce byla úspěšně provedena.')
        except Transaction.InsufficientFunds as e:
            messages.error(self.request, str(e))
        return super().form_valid(form)


class ChangeDefaultCurrencyBalance(BankView, View):
    def post(self, request, *args, **kwargs):
        account: Account = Account.objects.get(pk=self.kwargs['pk'])
        current_default_balance: AccountBalance = account.get_default_balance()
        new_default_balance: AccountBalance = account.get_balance(request.POST['currency'])
        new_default_balance.set_default()
        messages.success(
            request,
            f'Výchozí měna účtu byla změněna z {current_default_balance.currency} na {new_default_balance.currency}.'
        )
        return HttpResponseRedirect(reverse('bank:account-detail', kwargs={'pk': account.pk}))


class AddFundsView(BankView, View):
    def post(self, request, *args, **kwargs):
        account: Account = Account.objects.get(pk=self.kwargs['pk'])
        Transaction.objects.create_non_transfer(
            account, Transaction.TransactionType.DEPOSIT,
            float(request.POST['amount']), request.POST['currency'],
            request
        )
        return HttpResponseRedirect(reverse('bank:account-detail', kwargs={'pk': account.pk}))


class SubtractFundsView(BankView, View):
    def post(self, request, *args, **kwargs):
        account: Account = Account.objects.get(pk=self.kwargs['pk'])
        Transaction.objects.create_non_transfer(
            account, Transaction.TransactionType.WITHDRAWAL,
            float(request.POST['amount']), request.POST['currency'],
            request
        )
        return HttpResponseRedirect(reverse('bank:account-detail', kwargs={'pk': account.pk}))
