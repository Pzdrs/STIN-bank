from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from STINBank.views import BankView
from accounts.forms import PreferredCurrencyForm, UserForm
from accounts.models import User


# Create your views here.

class BankLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class BankLogoutView(LogoutView):
    template_name = 'logout.html'


class PreferencesView(BankView, TemplateView):
    template_name = 'preferences.html'

    def get_context_data(self, **kwargs):
        user: User = self.request.user
        context = super().get_context_data(**kwargs)
        context['preferred_currency_form'] = PreferredCurrencyForm(initial={
            'preferred_currency': user.preferred_currency
        })
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserForm(data=request.POST, instance=request.user)
        instance = user_form.save(commit=False)
        instance.save(update_fields=('preferred_currency',))
        return redirect(reverse('accounts:preferences'))
