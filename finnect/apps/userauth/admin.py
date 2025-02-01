from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from finnect.apps.userauth.models import User
from finnect.apps.userauth.forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = User
    list_display = [
        'email',
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'role',

    ]
    list_filter = ['email', 'is_staff', 'is_active', 'role']

    fieldsets = (
        (
            _('Login Credentials'),
            {
                "fields": (
                    "username",
                    "password",
                    "email",
                )
            }
        ),
        (
            _('Personal Information'),
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "id_number",
                    "role",
                )
            }
        ),
        (
            _('Account Status'),
            {
                "fields": (
                    "account_status",
                    "failed_login_attempts",
                    "last_failed_login",
                )
            }
        ),
        (
            _('Security'),
            {
                "fields": (
                    "security_question",
                    "security_answer",
                )
            }
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            }
        )
    )

    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['email']