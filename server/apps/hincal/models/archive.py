from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.hincal.services.archive import (
    get_cost_accounting,
    get_land_cadastral_value,
    get_property_cadastral_value, get_possible_income_from_patent,
    get_registration_costs,
)
from server.apps.services.base_model import AbstractBaseModel


class Archive(AbstractBaseModel):
    """Архив."""

    year = models.PositiveIntegerField(
        _('Год, к которому относятся данные')
    )
    land_tax_rate = models.FloatField(
        _('Размер налоговой ставки на землю'),
        default=0.015,
    )
    property_tax_rate = models.FloatField(
        _('Размер налогаовой ставки на имущество'),
        default=0.019,
    )
    patent_tax_rate = models.FloatField(
        _('Размер налоговой ставки по патенту'),
        default=0.06,
    )
    personal_income_rate = models.FloatField(
        _('Размер НДФЛ'),
        default=0.013,
    )
    pension_contributions_rate = models.FloatField(
        _('Размер ставки для пенсионных отчислений'),

        default=0.22,
    )
    medical_contributions_rate = models.FloatField(
        _('Размер ставки для медицинских отчислений'),
        default=0.051,
    )
    lower_tax_margin_error = models.FloatField(
        _('Нижний уровень погрешности для поиска записей по налогам'),
        default=0.9,
    )
    upper_tax_margin_error = models.FloatField(
        _('Верхний уровень погрешности для поиска записей по налогам'),
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
    cost_accounting = models.JSONField(
        _('Стоимость услуг на ведение бухгалтерского учета'),
        default=get_cost_accounting,
    )
    possible_income_from_patent = models.JSONField(
        _('Возможный доход для ИП по патентной системе'),
        default=get_possible_income_from_patent,
    )
    registration_costs = models.JSONField(
        _('Расходы на регистрацию бизнеса'),
        default=get_registration_costs,
    )
    avg_land_lease_costs = models.FloatField(
        _('Средняя стоимость аренды земли'),
        default=50,
    )
    avg_land_purchase_costs = models.FloatField(
        _('Средняя стоимость покупки земли'),
        default=100,
    )

    avg_property_lease_costs = models.FloatField(
        _('Средняя стоимость аренды недвижимости'),
        default=100,
    )
    avg_property_purchase_costs = models.FloatField(
        _('Средняя стоимость покупки недвижимости'),
        default=200,
    )
    avg_property_repair_costs = models.FloatField(
        _('Средняя стоимость капитального строительства недвижимости'),
        default=100,
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
        return f'{self.year}: {self.created_at}'
