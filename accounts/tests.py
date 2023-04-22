import os
from unittest.mock import patch, MagicMock

import png
import pyotp
import qrcode
from decouple import config
from django.conf import settings
from django.contrib.admin import AdminSite
from django.core.files import File
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse

from STINBank.utils.config import get_bank_config, get_project_config
from accounts.admin import AccountsUserAdmin
from accounts.forms import UserForm
from accounts.middleware import VerificationMiddleware
from accounts.models import User
from accounts.views import BankVerifyTOTPView
from bank.utils.currency import get_currency_display


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


class ModelAdminTests(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.request = MockRequest()
        self.request.user = MockSuperUser()

    def test_user_fieldsets(self):
        user_admin = AccountsUserAdmin(User, self.site)
        expected_fieldsets = [
            (None, {'fields': ('username', 'password')}),
            ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
            ('Important dates', {'fields': ('last_login', 'date_joined')}),
            ("Bank related data", {"fields": ("preferred_currency",)}),
            ("Security", {"fields": ("use_2fa",)}),
        ]

        self.assertEqual(user_admin.get_fieldsets(self.request, self.request.user), expected_fieldsets)

    def test_mock_super_user(self):
        su = MockSuperUser()
        self.assertTrue(su.has_perm('perm'))


class FormTests(TestCase):

    def test_user_form(self):
        form = UserForm()
        for field in form.fields.values():
            self.assertFalse(field.required)


class MiddlewareTests(TestCase):
    def setUp(self):
        self.middleware = VerificationMiddleware(lambda r: HttpResponse())
        self.user: User = User.objects.create_user(username='test', password='test')
        self.factory = RequestFactory()

    def test_pending_verification_with_2fa(self):
        self.user.set_pending_verification(True)
        self.user.use_2fa = True
        self.user.save()

        self.client.login(username='test', password='test')
        response = self.client.get(reverse('bank:dashboard'))

        # we should be redirected to the verification page
        self.assertRedirects(response, reverse('accounts:login-totp-verify'))

        # if we try to access the dashboard, we should be redirected to the verification page again
        dashboard_response = self.client.get(reverse('bank:dashboard'))
        self.assertRedirects(dashboard_response, reverse('accounts:login-totp-verify'))

    def test_pending_verification_without_2fa(self):
        self.user.set_pending_verification(True)
        self.user.use_2fa = False
        self.user.save()

        self.client.login(username='test', password='test')

        request = self.factory.get(reverse('bank:dashboard'))
        request.user = self.user
        middleware_response = self.middleware(request)

        # We shouldn't be redirected to the verification page
        self.assertEqual(middleware_response.status_code, 200)

        # The user should no longer have a pending verification
        self.assertFalse(self.user.has_pending_verification())


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(username='test', password='test')

    def test_get_preferred_currency_display(self):
        self.user.preferred_currency = 'EUR'
        self.assertEqual(self.user.get_preferred_currency_display(), get_currency_display('EUR'))

    def test_has_preferred_currency(self):
        self.assertFalse(self.user.has_preferred_currency())
        self.user.preferred_currency = 'EUR'
        self.assertTrue(self.user.has_preferred_currency())

    def test_get_full_name_reversed__no_name(self):
        self.assertEqual(self.user.get_full_name_reversed(), '')

    def test_get_full_name_reversed__first_name(self):
        self.user.first_name = 'John'
        self.assertEqual(self.user.get_full_name_reversed(), 'John')

    def test_get_full_name_reversed__last_name(self):
        self.user.last_name = 'Doe'
        self.assertEqual(self.user.get_full_name_reversed(), 'Doe')

    def test_get_full_name_reversed__first_and_last_name(self):
        self.user.first_name = 'John'
        self.user.last_name = 'Doe'
        self.assertEqual(self.user.get_full_name_reversed(), 'Doe John')

    def test_otp_provisioning(self):
        self.assertEqual(
            self.user.get_totp_uri(),
            f'otpauth://totp/{get_bank_config().name}:{self.user.username}?secret={config("TOTP_KEY")}&issuer={get_bank_config().name}'
        )

    def test_qrcode_deletion_on_delete(self):
        # Create a user object and generate a qrcode for them
        user = User.objects.create(username='testuser')
        qrcode_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', f'{user.pk}.png')
        with open(qrcode_path, 'w') as f:
            f.write('test qrcode')
        # Check that the qrcode file exists
        self.assertTrue(os.path.exists(qrcode_path))
        # Delete the user
        user.delete()
        # Check that the user was deleted and the qrcode file was deleted
        self.assertFalse(User.objects.filter(pk=user.pk).exists())
        self.assertFalse(os.path.exists(qrcode_path))

    def test_qrcode_generation(self):
        # Create a user object
        user = User.objects.create(username='testuser')
        # Call the generate_qr_code task
        from accounts.tasks import generate_qr_code
        generate_qr_code(user.pk)
        # Check that the qrcode file exists
        qrcode_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', f'{user.pk}.png')
        self.assertTrue(os.path.exists(qrcode_path))


class ViewTests(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(username='test', password='test')
        self.client.user = self.user
        self.factory = RequestFactory()

    def test_bank_login_view_no_2fa(self):
        response = self.client.post(reverse('accounts:login'), {'username': 'test', 'password': 'test'})
        self.assertRedirects(response, reverse('bank:dashboard'))

    def test_bank_login_view_2fa(self):
        self.user.use_2fa = True
        self.user.save()

        response = self.client.post(reverse('accounts:login'), {'username': 'test', 'password': 'test'})
        self.assertRedirects(response, reverse('accounts:login-totp-verify'))

    def test_totp_verify_view_get__no_referrer(self):
        self.client.login(username='test', password='test')
        # not using 2fa - should be redirected to default page
        response = self.client.get(reverse('accounts:login-totp-verify'))
        self.assertRedirects(response, get_project_config().default_page)

    def test_totp_verify_view_get__with_referrer(self):
        self.client.login(username='test', password='test')
        # not using 2fa - should be redirected to previous page
        response = self.client.get(reverse('accounts:login-totp-verify'), HTTP_REFERER=reverse('bank:dashboard'))
        self.assertRedirects(response, reverse('bank:dashboard'))

    def test_totp_verify_view_post_no_data(self):
        self.client.login(username='test', password='test')
        # no data - shouldn't crash
        response = self.client.post(reverse('accounts:login-totp-verify'))
        self.assertIsInstance(response, TemplateResponse)

    def test_totp_verify_view_post__verify_fail(self):
        self.client.login(username='test', password='test')
        response = self.client.post(reverse('accounts:login-totp-verify'), {'code': '123456'})
        # the post method should return super().get(request, *args, **kwargs)
        self.assertIsInstance(response, TemplateResponse)

    def test_totp_verify_view_post__verify_pass(self):
        totp = pyotp.TOTP(config('TOTP_KEY'))
        code = totp.now()
        self.user.set_pending_verification(True)
        self.assertTrue(self.user.has_pending_verification())

        request = self.factory.post(reverse('bank:dashboard'), {'code': code})
        request.user = self.user

        response = BankVerifyTOTPView.as_view()(request)
        # because we passed the verification, we should be redirected to the default page
        self.assertEqual(response.url, get_project_config().default_page)
        # the user should no longer have a pending verification
        self.assertFalse(self.user.has_pending_verification())

    def test_password_change_success(self):
        self.client.login(username='test', password='test')
        url = reverse('accounts:password_change')
        data = {'old_password': 'test', 'new_password1': 'new_password', 'new_password2': 'new_password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:preferences'))

    def test_user_preferences_post(self):
        self.client.login(username='test', password='test')

        data = {
            'username': 'test',
            'email': 'testuser2@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = self.client.post( reverse('accounts:preferences'), data)
        self.assertEqual(response.status_code, 302)  # success redirects to success_url
        self.assertRedirects(response, reverse('accounts:preferences'))

        # Check that the user was updated with the new data
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, data['username'])
        self.assertEqual(updated_user.email, data['email'])
        self.assertEqual(updated_user.first_name, data['first_name'])
        self.assertEqual(updated_user.last_name, data['last_name'])
