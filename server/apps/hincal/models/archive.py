from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.hincal.services.archive import (
    get_cost_accounting,
    get_cost_capital_construction,
    get_land_cadastral_value,
    get_property_cadastral_value,
)
from server.apps.services.base_model import AbstractBaseModel


class Archive(AbstractBaseModel):
    """Архив."""

    year = models.PositiveIntegerField(
        _('Год, к которому относятся данные')
    )
    land_tax_rate = models.DecimalField(
        _('Размер налога на землю'),
        max_digits=5,
        decimal_places=3,
        default=0.015,
    )

    property_tax_rate = models.DecimalField(
        _('Размер налога на имущество'),
        max_digits=5,
        decimal_places=3,
        default=0.019,
    )
    lower_tax_margin_error = models.DecimalField(
        _('Нижний уровень погрешности для поиска записей по налогам'),
        max_digits=5,
        decimal_places=3,
        default=0.9,
    )
    upper_tax_margin_error = models.DecimalField(
        _('Верхний уровень погрешности для поиска записей по налогам'),
        max_digits=5,
        decimal_places=3,
        default=1.1,
    )
    land_cadastral_value = models.JSONField(
        _('Кадастровая стоимость земли'),
        default=get_land_cadastral_value,
    )
    property_cadastral_value = models.JSONField(
        _('Кадастровая стоимость имущества'),
        default=get_property_cadastral_value,
    )
    cost_capital_construction = models.JSONField(
        _('Стоимость капитального строительства промышленного объекта'),
        default=get_cost_capital_construction,
    )
    cost_accounting = models.JSONField(
        _('Стоимость услуг на ведение бухгалтерского учета'),
        default=get_cost_accounting,
    )
    is_actual = models.BooleanField(
        _('Актуальные данные в архиве или нет'),
        default=True
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Архив')
        verbose_name_plural = _('Архивы')
        constraints = [
            models.UniqueConstraint(
                name='unique_is_actual_for_archive',
                condition=models.Q(('is_actual', True)),
                fields=('is_actual',)
            ),
        ]

    def __str__(self):
        return f'{self.user}: {self.created_at}'
