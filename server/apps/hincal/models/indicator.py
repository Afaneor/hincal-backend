from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel


class Indicator(AbstractBaseModel):
    """Экономические показатели ИП, физического лица или компании."""

    business = models.ForeignKey(
        'hincal.Business',
        on_delete=models.CASCADE,
        verbose_name=_('Бизнес'),
        related_name='indicators',
        db_index=True,
        null=True,
    )
    year = models.IntegerField(
        _('Год, к которому относятся показатели'),
    )
    average_number_of_employees = models.DecimalField(
        _('Среднесписочная численность персонала'),
        max_digits=20,
        decimal_places=3,
        null=True,
    )
    average_salary_of_employees = models.DecimalField(
        _('Средняя заработная плата сотрудника'),
        max_digits=20,
        decimal_places=3,
        null=True,
    )
    taxes_to_the_budget = models.DecimalField(
        _('Налоги, уплаченные в бюджет Москвы'),
        max_digits=20,
        decimal_places=3,
        null=True,
    )
    income_tax = models.DecimalField(
        _('Налог на прибыль'),
        max_digits=20,
        decimal_places=3,
        null=True,
    )
    property_tax = models.DecimalField(
        _('Налог на имущество'),
        max_digits=20,
        decimal_places=3,
        null=True,
    )
    land_tax = models.DecimalField(
        _('Налог на землю'),
        max_digits=20,
        decimal_places=3,
        null=True,
    )
    personal_income_tax = models.DecimalField(
        _('НДФЛ'),
        max_digits=20,
        decimal_places=3,
        null=True,
    )
    transport_tax = models.DecimalField(
        _('Транспортный налог'),
        max_digits=20,
        decimal_places=3,
        null=True,
    )
    other_taxes = models.DecimalField(
        _('Прочие налоги'),
        max_digits=20,
        decimal_places=3,
        null=True,
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Индикатор бизнеса')
        verbose_name_plural = _('Индикаторы бизнесов')
        constraints = [
            models.UniqueConstraint(
                name='unique_yer_for_business',
                fields=('year', 'business'),
            ),
        ]

    def __str__(self):
        return f'{self.business}. Год - {self.year}'
