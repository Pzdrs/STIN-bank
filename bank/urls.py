from django.urls import path

from bank.views import DashboardView

app_name = 'bank'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('account/<int:pk>/', DashboardView.as_view(), name='account-detail'),
    path('account/<int:pk>/history', DashboardView.as_view(), name='account-history'),
    path('account/<int:pk>/payment', DashboardView.as_view(), name='account-payment'),
]
