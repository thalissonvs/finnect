import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from finnect.apps.userauth.utils import send_account_blocked_email
from finnect.apps.userauth.managers import CustomUserManager


class User(AbstractUser):
    class SecurityQuestions(models.TextChoices):
        MAIDEN_NAME = (
            "maiden_name",
            _("What's your mother's maiden name?")
        )
        FAVORITE_COLOR = (
            "favorite_color",
            _("What's your favorite color?")
        )
        BIRTH_CITY = (
            "birth_city",
            _("What's the city where you were born?")
        )
        CHILDHOOD_FRIEND = (
            "childhood_friend",
            _("What's the name of your childhood best friend?")
        )
    
    class AccountStatus(models.TextChoices):
        ACTIVE = "ative", _("Active")
        BLOCKED = "blocked", _("Blocked")

    class RoleChoices(models.TextChoices):
        CUSTOMER = "customer", _("Customer")
        EXECUTIVE = "executive", _("Account Executive")
        TELLER = "teller", _("Teller")
        BRANCH_MANAGER = "branch_manager", _("Branch Manager")
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_("Username"), max_length=12, unique=True)
    security_question = models.CharField(
        _("Security Question"),
        max_length=30,
        choices=SecurityQuestions.choices
    )
    security_answer = models.CharField(
        _("Security Answer"),
        max_length=30
    )
    email = models.EmailField(_("Email"), unique=True, db_index=True)
    first_name = models.CharField(_("First Name"), max_length=30)
    middle_name = models.CharField(
        _("Middle Name"), max_length=30, blank=True, null=False, default=""
    )
    last_name = models.CharField(
        _("Last Name"), max_length=30
    )
    id_number = models.PositiveIntegerField(_("ID Number"), unique=True)
    account_status = models.CharField(
        _("Account Status"),
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE
    )
    role = models.CharField(
        _("Role"),
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.CUSTOMER
    )
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    otp = models.CharField(
        _("OTP"),
        max_length=6,
        blank=True
    )
    otp_expiration_time = models.DateTimeField(
        _("OTP Expiration Time"),
        null=True,
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "id_number",
        "security_question",
        "security_answer",
    ]

    def set_otp(self, otp: str) -> None:
        self.otp = otp
        self.otp_expiration_time = timezone.now() + settings.OTP_EXPIRATION
        self.save()
    
    def verify_otp(self, otp: str) -> bool:
        if self.otp == otp and self.otp_expiration_time > timezone.now():
            self.otp = ""
            self.otp_expiration_time = None
            self.save()
            return True
        return False