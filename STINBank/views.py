from django.contrib.auth.mixins import AccessMixin


class BankView(AccessMixin):
    title: str = None
    page_title: str = None
    page_subtitle: str = None
    login_required: bool = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = self.get_title()
        context['page_title'] = self.get_page_title()
        context['page_subtitle'] = self.get_page_subtitle()

        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and self.login_required:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_title(self):
        return self.title

    def get_page_title(self):
        return self.page_title

    def get_page_subtitle(self):
        return self.page_subtitle
