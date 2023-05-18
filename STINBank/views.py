from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from STINBank.utils.config import get_project_config


class BankView(AccessMixin):
    title: str = None
    login_required: bool = True

    def test_func(self, request: HttpRequest, *args, **kwargs):
        """
        Yoinked from the Django built-in UserPassesTestMixin
        """
        pass

    def handle_test_fail(self, request) -> HttpResponse:
        messages.error(request, 'Nemáte oprávnění k přístupu na tuto stránku.')
        try:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        except KeyError:
            return HttpResponseRedirect(get_project_config().default_page)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = self.get_title()

        return context

    def dispatch(self, request, *args, **kwargs):
        test_func = self.test_func(request, *args, **kwargs)
        if test_func is not None and not test_func:
            return self.handle_test_fail(request)
        if not request.user.is_authenticated and self.login_required:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_title(self):
        return self.title
