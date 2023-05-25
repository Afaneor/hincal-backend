from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel


class Report(AbstractBaseModel):
    """Отчет."""

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='reports',
        db_index=True,
        null=True,
    )
    initial_data = models.JSONField(
        _('Исходные данные по которым был сформирован отчет'),
    )
    context = models.JSONField(
        _('Данные для формирования отчета'),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Отчет')
        verbose_name_plural = _('Отчеты')

    def __str__(self):
        return f'{self.user}: {self.created_at}'
