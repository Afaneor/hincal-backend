from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.hincal.models import Report
from server.apps.services.base_model import AbstractBaseModel


class Statistic(AbstractBaseModel):
    """Общая статистика по системе и для пользователя."""

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='statistics',
        db_index=True,
        null=True,
    )
    popular_sector = models.CharField(
        _('Популярная отрасль для инвестирования'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    average_investment_amount = models.DecimalField(
        _('Средняя сумма инвестирования'),
        max_digits=20,
        decimal_places=3,
        null=True,
    )
    total_investment_amount = models.DecimalField(
        _('Общая сумма инвестирования'),
        max_digits=20,
        decimal_places=3,
        null=True,
    )
    amount_of_use_of_the_calculator = models.PositiveIntegerField(
        _('Сколько раз использовался калькулятор'),
        default=0,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Статистика')
        verbose_name_plural = _('Статистика')

    def __str__(self):
        return f'{self.user}'

    @property
    def number_of_reports(self):
        """Количество отчетов."""
        return Report.objects.all().count()

