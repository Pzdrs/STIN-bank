from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class VerificationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check if user has a pending verification
            if request.user.has_pending_verification():
                if settings.ENABLE_2FA:
                    # Redirect to verification page
                    verification_url = reverse('accounts:login-totp-verify')
                    if request.path != verification_url:
                        return redirect(verification_url)
                else:
                    request.user.set_pending_verification(False)

        response = self.get_response(request)
        return response
