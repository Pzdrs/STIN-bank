from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.

class BankLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class BankLogoutView(LogoutView):
    template_name = 'logout.html'
