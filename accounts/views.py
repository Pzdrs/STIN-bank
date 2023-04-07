import pyotp
from decouple import config
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from STINBank.utils.config import get_project_config
from STINBank.views import BankView
from accounts.forms import PreferredCurrencyForm, UserForm
from accounts.models import User


# Create your views here.

class BankLoginView(BankView, LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    login_required = False
    title = 'Přihlašte se'

    def get_success_url(self):
        return reverse('accounts:login-totp-verify') if settings.ENABLE_2FA else reverse('bank:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        user: User = self.request.user
        if settings.ENABLE_2FA:
            user.set_pending_verification(True)
        return response

    def post(self, request, *args, **kwargs):
        uri = pyotp.totp.TOTP(config('TOTP_KEY')).provisioning_uri(
            name=request.user.username,
            issuer_name='STINBank'
        )
        print(uri)
        return super().post(request, *args, **kwargs)


class BankVerifyTOTPView(BankView, TemplateView):
    template_name = 'verify_totp.html'
    title = 'Ověření uživatele'

    def get(self, request, *args, **kwargs):
        if not settings.ENABLE_2FA or (settings.ENABLE_2FA and not request.user.has_pending_verification()):
            try:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            except KeyError:
                return HttpResponseRedirect(get_project_config().default_page)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        totp = pyotp.TOTP(config('TOTP_KEY'))
        if not totp.verify(request.POST['code']):
            return super().get(request, *args, **kwargs)
        request.user.set_pending_verification(False)
        return redirect(get_project_config().default_page)


class BankLogoutView(BankView, LogoutView):
    template_name = 'logout.html'
    title = 'Odhlášen'


class PreferencesView(BankView, TemplateView):
    template_name = 'preferences.html'
    title = 'Nastavení'

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


class BankPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('accounts:preferences')

    def form_valid(self, form):
        messages.success(self.request, 'Heslo úspěšně změněno.')
        return super().form_valid(form)
