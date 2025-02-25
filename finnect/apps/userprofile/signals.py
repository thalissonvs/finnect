from typing import Any, Type

from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from loguru import logger
from django.conf import settings
from finnect.apps.userprofile.models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender: Type[Model], instance: Model, created: bool, **kwargs: Any) -> None:
    """
    Cria um perfil de usuário quando um novo usuário é criado.
    """
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"Profile created for user {instance.first_name} {instance.last_name}")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender: Type[Model], instance: Model, **kwargs: Any) -> None:
    """
    Salva o perfil de usuário quando o usuário é salvo.
    """
    instance.profile.save()
    logger.info(f"Profile saved for user {instance.first_name} {instance.last_name}")