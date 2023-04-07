from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path

from accounts.views import BankLogoutView, BankLoginView, PreferencesView, BankPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path("login/", BankLoginView.as_view(), name="login"),
    path("logout/", BankLogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        BankPasswordChangeView.as_view(),
        name="password_change"
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path('preferences/', PreferencesView.as_view(), name='preferences')
]
