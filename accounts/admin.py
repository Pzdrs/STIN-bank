from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from accounts.models import User

@admin.register(User)
class UserAdmin(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))
        fieldsets.append(
            (_("Bank related data"), {"fields": ("preferred_currency",)}),
        )
        return fieldsets