from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from server.apps.services.base_model import AbstractBaseModel


class Area(AbstractBaseModel):
    """Площадки для осуществления деятельности."""

    preview_image = models.CharField(
        _('Изображение'),
        blank=True,
    )
    title = models.CharField(
        _('Заголовок'),
        max_length=settings.MAX_STRING_LENGTH,
    )
    text = models.CharField(
        _('Краткое описание объекта'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    territorial_location = models.ForeignKey(
        'hincal.TerritorialLocation',
        on_delete=models.CASCADE,
        verbose_name=_('Территориальное положение площадки'),
        related_name='areas',
        null=True,
        blank=True,
    )
    address = models.CharField(
        _('Адрес площадки'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    site = models.URLField(
        _('Ссылка на сторонний ресурс с подробной информацией'),
        blank=True,
    )
    tags = TaggableManager(blank=True)

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Площадка для осуществления деятельности')
        verbose_name_plural = _('Площадки для осуществления деятельности')

    def __str__(self):
        return self.title
