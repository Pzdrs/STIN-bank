from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from STINBank.utils.config import get_project_config
from accounts.views import BankLogoutView, BankLoginView, PreferencesView, BankPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path("login/", BankLoginView.as_view(), name="login"),
    path("logout/", BankLogoutView.as_view(), name="logout"),
    path(
        "password_change/", BankPasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", PasswordResetView.as_view(
        success_url=get_project_config().default_page
    ), name="password_reset"),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path('preferences/', PreferencesView.as_view(), name='preferences')
]
