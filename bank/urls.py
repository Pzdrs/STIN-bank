from django.urls import path

from bank.views import DashboardView

app_name = 'bank'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
