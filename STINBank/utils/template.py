from django.contrib import messages
from django.forms import Form
from django.http import HttpRequest


def push_form_errors_to_messages(request: HttpRequest, form: Form):
    for field, errors in form.errors.items():
        for error in errors:
            if field == '__all__':
                messages.error(request, error)
            else:
                messages.error(request, f'<b>{field}</b>: {error}')
