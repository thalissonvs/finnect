from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from finnect.apps.userauth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'email',
            'id_number',
            'first_name',
            'middle_name',
            'last_name',
            'security_question',
            'security_answer',
            'is_staff',
            'is_superuser',
        ]
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('A user with this email already exists.'))
        return email
    
    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')
        if User.objects.filter(id_number=id_number).exists():
            raise ValidationError(_('A user with this ID number already exists.'))
        return id_number
    
    def clean(self):
        cleaned_data = super().clean()
        is_superuser = cleaned_data.get('is_superuser')
        security_question = cleaned_data.get('security_question')
        security_answer = cleaned_data.get('security_answer')

        if not is_superuser and not security_question:
            self.add_error('security_question', _('Security question is required for regular users.'))
        
        if not is_superuser and not security_answer:
            self.add_error('security_answer', _('Security answer is required for regular users.'))
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'email',
            'id_number',
            'first_name',
            'middle_name',
            'last_name',
            'security_question',
            'security_answer',
            'is_active',
            'is_staff',
            'is_superuser',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError(_('A user with this email already exists.'))
        return email

    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')
        if User.objects.exclude(pk=self.instance.pk).filter(id_number=id_number).exists():
            raise ValidationError(_('A user with this ID number already exists.'))
        return id_number
    
    def clean(self):
        cleaned_data = super().clean()
        is_superuser = cleaned_data.get('is_superuser')
        security_question = cleaned_data.get('security_question')
        security_answer = cleaned_data.get('security_answer')

        if not is_superuser and not security_question:
            self.add_error('security_question', _('Security question is required for regular users.'))
        
        if not is_superuser and not security_answer:
            self.add_error('security_answer', _('Security answer is required for regular users.'))
        
        return cleaned_data