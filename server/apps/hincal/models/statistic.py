from tortoise import models, fields

from app import config


class Statistic(models.Model):
    """Глобальная статистика по системе."""

    id = fields.IntField(pk=True)
    popular_sector = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Популярная отрасль для инвестирования',
    )
    average_investment_amount = fields.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        description='Средняя сумма инвестирования',
    )
    total_investment_amount = fields.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        description='Общая сумма инвестирования',
    )

    def __str__(self):
        return f'{self.popular_sector}'
