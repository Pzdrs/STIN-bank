from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from accounts.models import User


class VerificationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

    def __call__(self, request: HttpRequest):
        user: User = request.user
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check if user has a pending verification
            if user.has_pending_verification():
                if user.is_using_2fa():
                    # Redirect to verification page
                    verification_url = reverse('accounts:login-totp-verify')
                    if request.path != verification_url:
                        return redirect(verification_url)
                else:
                    user.set_pending_verification(False)
        return self.get_response(request)
