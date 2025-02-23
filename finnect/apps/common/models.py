import uuid
from typing import Any, Optional
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # define que a classe é abstrata, ou seja, não será criada uma tabela
        #  no banco de dados e sim será usada como modelo base para outras classes.
        abstract = True


class ContentView(TimeStampedModel):
    """
    Modelo para rastrear visualizações de diferentes tipos de conteúdo na aplicação.

    Este modelo utiliza ContentType e GenericForeignKey para criar relacionamentos
    genéricos com qualquer modelo da aplicação. Isso permite rastrear visualizações
    de diferentes tipos de objetos (posts, produtos, etc) em uma única tabela.

    Attributes:
        content_type (ForeignKey): Referência ao modelo ContentType que identifica
            o tipo do objeto sendo visualizado.
        object_id (UUIDField): UUID do objeto específico sendo visualizado.
        content_object (GenericForeignKey): Campo especial que combina content_type
            e object_id para fornecer acesso direto ao objeto relacionado.
        user (ForeignKey): Usuário opcional que realizou a visualização.

    Exemplo de Uso:
        >>> from django.contrib.contenttypes.models import ContentType
        >>> # Registrando visualização de um post
        >>> post = Post.objects.get(id='123e4567-e89b-12d3-a456-426614174000')
        >>> ContentView.objects.create(
        ...     content_type=ContentType.objects.get_for_model(Post),
        ...     object_id=post.id,
        ...     user=request.user
        ... )
        
        >>> # Consultando visualizações
        >>> # Todas as visualizações de um post específico
        >>> views = ContentView.objects.filter(
        ...     content_type=ContentType.objects.get_for_model(Post),
        ...     object_id=post.id
        ... )
        
        >>> # Visualizações por usuário
        >>> user_views = ContentView.objects.filter(user=user)
        
        >>> # Acessando o objeto relacionado
        >>> view = ContentView.objects.first()
        >>> related_object = view.content_object  # Retorna o objeto visualizado
    """
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_('Content Type')
    )
    object_id = models.UUIDField(verbose_name=_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='content_views',
        verbose_name=_('User')
    )
    viewer_ip = models.GenericIPAddressField(
        null=True, blank=True, verbose_name=_('Viewer IP')
    )
    last_viewed = models.DateTimeField()

    class Meta:
        verbose_name = _('Content View')
        verbose_name_plural = _('Content Views')
        # Impede que um usuário com o mesmo IP registre visualizações repetidas
        # no banco de dados para o mesmo objeto.
        unique_together = ['content_type', 'object_id', 'user', 'viewer_ip']

    def __str__(self) -> str:
        return (
            f'{self.content_type} viewed by {self.user.get_full_name() if self.user else "Anonymous"} '
            f'from IP {self.viewer_ip}'
        )
    
    @classmethod
    def record_view(
        cls,
        content_object: Any,
        user: Optional[User],
        viewer_ip: Optional[str] = None
    ) -> None:
        content_type = ContentType.objects.get_for_model(content_object)
        try:
            view, created = cls.objects.get_or_create(
                content_type=content_type,
                object_id=content_object.id,
                user=user,
                viewer_ip=viewer_ip,
                defaults={'last_viewed': timezone.now()}
            )
            if not created:
                view.last_viewed = timezone.now()
                view.save()
            
        except IntegrityError:
            pass
    