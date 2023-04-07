from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from accounts.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "use_2fa", "pending_verification")

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))
        fieldsets.extend((
            (_("Bank related data"), {"fields": ("preferred_currency",)}),
            (_("Security"), {"fields": ("use_2fa",)}),
        ))
        return fieldsets
