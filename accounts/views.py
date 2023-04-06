from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

from STINBank.views import BankView


# Create your views here.

class BankLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class BankLogoutView(LogoutView):
    template_name = 'logout.html'


class PreferencesView(BankView, TemplateView):
    template_name = 'preferences.html'
