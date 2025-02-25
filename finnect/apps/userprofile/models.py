from typing import Any

from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


from finnect.apps.common.models import TimeStampedModel


User = get_user_model()


class Profile(TimeStampedModel):
    """
    Classe para representar o perfil de um usuário. Contém informações
    sobre KYC (Know Your Customer) e outras informações pessoais.
    """

    class Salutation(models.TextChoices):
        MR = ('mr', _('Mr.'))
        MRS = ('mrs', _('Mrs.'))
        MISS = ('miss', _('Miss'))

    class Gender(models.TextChoices):
        MALE = ('male', _('Male'))
        FEMALE = ('female', _('Female'))
        OTHER = ('other', _('Other'))

    class MaritalStatus(models.TextChoices):
        SINGLE = ('single', _('Single'))
        MARRIED = ('married', _('Married'))
        DIVORCED = ('divorced', _('Divorced'))
        WIDOWED = ('widowed', _('Widowed'))
        SEPARETED = ('separated', _('Separated'))
        UNKNOWN = ('unknown', _('Unknown'))

    class IdentificationMeans(models.TextChoices):
        PASSPORT = ('passport', _('Passport'))
        NATIONAL_ID = ('national_id', _('National ID'))
        DRIVERS_LICENSE = ('drivers_license', _("Driver's License"))

    class EmploymentStatus(models.TextChoices):
        SELF_EMPLOYED = ('self_employed', _('Self-Employed'))
        EMPLOYED = ('employed', _('Employed'))
        UNEMPLOYED = ('unemployed', _('Unemployed'))
        RETIRED = ('retired', _('Retired'))
        STUDENT = ('student', _('Student'))

    # o campo related_name permite cria um relação inversa, permitindo
    # acessar o perfil de um usuário a partir do modelo User. O default é
    # `profile_set`, mas podemos alterar para `profile` para facilitar o acesso.
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    title = models.CharField(
        _('Salutation'),
        max_length=5,
        choices=Salutation.choices,
        default=Salutation.MR,
    )
    gender = models.CharField(
        _('Gender'), max_length=8, choices=Gender.choices, default=Gender.MALE
    )
    date_of_birth = models.DateField(_('Date of Birth'))
    coutry_of_birth = CountryField(_('Country of Birth', default='BR'))
    place_of_birth = models.CharField(_('Place of Birth'), max_length=255)
    marital_status = models.CharField(
        _('Marital Status'),
        max_length=10,
        choices=MaritalStatus.choices,
        default=MaritalStatus.SINGLE,
    )
    identification_means = models.CharField(
        _('Identification Means'),
        max_length=15,
        choices=IdentificationMeans.choices,
        default=IdentificationMeans.PASSPORT,
    )
    identification_issue_date = models.DateField(_('Issue Date'))
    identification_expiry_date = models.DateField(_('Expiry Date'))
    passport_number = models.CharField(
        _('Passport Number'), max_length=20, blank=True, null=True
    )
    nationality = models.CharField(
        _('Nationality'), max_length=30, default='Unknown'
    )
    phone_number = PhoneNumberField(_('Phone Number'))
    address = models.TextField(_('Address'), max_length=100, default='Unknown')
    city = models.CharField(_('City'), max_length=50, default='Unknown')
    country = CountryField(_('Country'), default='BR')
    employment_status = models.CharField(
        _('Employment Status'),
        max_length=15,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.EMPLOYED,
    )
    employer_name = models.CharField(
        _('Employer Name'), max_length=100, blank=True, null=True
    )
    annual_income = models.DecimalField(
        _('Annual Income'),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    date_of_employment = models.DateField(
        _('Date of Employment', blank=True, null=True)
    )
    employer_address = models.CharField(
        _('Employer Address'), max_length=100, blank=True, null=True
    )
    employer_city = models.CharField(
        _('Employer City'), max_length=50, blank=True, null=True
    )
    employer_state = models.CharField(
        _('Employer State'), max_length=50, blank=True, null=True
    )
    photo = CloudinaryField(
        _('Photo'),
        blank=True,
        null=True,
    )
    photo_url = models.URLField(_('Photo URL'), blank=True, null=True)
    id_photo = CloudinaryField(
        _('ID Photo'),
        blank=True,
        null=True,
    )
    id_photo_url = models.URLField(_('ID Photo URL'), blank=True, null=True)
    signature_photo = CloudinaryField(
        _('Signature Photo'),
        blank=True,
        null=True,
    )
    signature_photo_url = models.URLField(
        _('Signature Photo URL'), blank=True, null=True
    )
