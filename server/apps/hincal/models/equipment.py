from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel


class Equipment(AbstractBaseModel):
    """Оборудование."""

    name = models.CharField(
        _('Название оборудования'),
        unique=True,
    )
    cost = models.DecimalField(
        _('Стоимость оборудования'),
        max_digits=10,
        decimal_places=3,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Оборудование')
        verbose_name_plural = _('Оборудования')

    def __str__(self):
        return f'{self.name}'
