from django.views.generic import TemplateView

from STINBank.views import BankView


# Create your views here.

class DashboardView(BankView, TemplateView):
    template_name = 'dashboard.html'
    title = 'Dashboard'
