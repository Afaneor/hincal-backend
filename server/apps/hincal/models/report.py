from tortoise import models, fields


class Report(models.Model):
    """Отчет."""

    id = fields.IntField(pk=True)
    account = fields.ForeignKeyField(
        'models.User',
        related_name='reports',
    )
    initial_data = fields.JSONField(
        description='Исходные данные по которым был сформирован отчет',
    )
    context = fields.JSONField(
        description='Данные для формирования отчета',
    )
    created = fields.DatetimeField(
        auto_now_add=True,
        description='Дата создания отчета в БД',
    )

    def __str__(self):
        return f'{self.accout}: {self.created}'
