from django.shortcuts import redirect
from django.urls import path

from STINBank.utils.config import get_project_config
from bank.views import DashboardView, AccountDetailView, AccountTransactionHistoryView, AccountTransactionView, \
    ChangeDefaultCurrencyBalance

app_name = 'bank'

urlpatterns = [
    path('', lambda request: redirect(get_project_config().default_page, permanent=True)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('account/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('account/<int:pk>/history', AccountTransactionHistoryView.as_view(), name='account-history'),
    path('account/<int:pk>/transaction', AccountTransactionView.as_view(), name='account-transaction'),
    path(
        'account/<int:pk>/change-default-currency',
        ChangeDefaultCurrencyBalance.as_view(),
        name='account-change-default-currency'
    )
]
