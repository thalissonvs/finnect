from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserprofileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "finnect.apps.userprofile"
    verbose_name = _("User Profile")
