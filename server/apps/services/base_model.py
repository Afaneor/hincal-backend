from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModelBase, RulesModelMixin


class AbstractBaseModel(  # type: ignore
    RulesModelMixin,
    models.Model,
    metaclass=RulesModelBase,
):
    """Базовая модель."""

    creator = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь - создатель объекта'),
        related_name='%(class)s_created_objects',  # noqa: WPS323
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Изменен'), auto_now=True)

    class Meta(object):
        abstract = True
        ordering = ['-id']


class AbstractContentTypeModel(models.Model):
    """Базовая модель, которая использует ContentType."""

    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('Тип содержимого'),
        on_delete=models.CASCADE,
        db_index=True,
        limit_choices_to=models.Q(
            models.Q(app_label='cicada', model='domain') |
            models.Q(app_label='cicada', model='ipaddress') |
            models.Q(app_label='cicada', model='leak') |
            models.Q(app_label='cicada', model='phishingresource') |
            models.Q(app_label='cicada', model='service') |
            models.Q(app_label='cicada', model='vulnerability'),
        ),
    )
    object_id = models.PositiveIntegerField(_('Id объекта'))
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta(object):
        abstract = True
