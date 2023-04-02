from django.views.generic import TemplateView

from STINBank.views import BankView
from bank.models import Account
from bank.utils.cnb import update_rates


# Create your views here.

class DashboardView(BankView, TemplateView):
    template_name = 'dashboard.html'
    title = 'Dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['accounts'] = Account.objects.for_user(self.request.user)
        update_rates()

        return context
