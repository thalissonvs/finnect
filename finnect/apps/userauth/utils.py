import random
import string

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from loguru import logger


def generate_otp(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))


def send_otp_email(email, otp):
    subject = _('Your OTP code')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        'otp': otp,
        'otp_expiration': settings.OTP_EXPIRATION,
        'site_name': settings.SITE_NAME,
    }
    html_email = render_to_string('emails/otp_email.html', context)
    text_email = strip_tags(html_email)
    msg = EmailMultiAlternatives(subject, text_email, from_email, recipient_list)
    msg.attach_alternative(html_email, "text/html")
    try:
        msg.send()
        logger.info(f'OTP email sent successfully to: {email}')
    except Exception as exc:
        logger.error(f'Error sending OTP email to {email}: {exc}')


def send_account_blocked_email(email, user):
    subject = _('Your account has been blocked')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        'user': user,
        'lockout_duration': int(settings.LOCKOUT_DURATION.total_seconds() // 60),
        'site_name': settings.SITE_NAME,
    }
    html_email = render_to_string('emails/account_blocked.html', context)
    text_email = strip_tags(html_email)
    msg = EmailMultiAlternatives(subject, text_email, from_email, recipient_list)
    msg.attach_alternative(html_email, "text/html")
    try:
        msg.send()
        logger.info(f'Account blocked email sent successfully to: {email}')
    except Exception as exc:
        logger.error(f'Error sending account blocked email to {email}: {exc}')
