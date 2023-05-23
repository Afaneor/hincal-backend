from tortoise import models, fields


class Indicator(models.Model):
    """Экономические показатели ИП или компании."""

    id = fields.IntField(pk=True)
    business = fields.ForeignKeyField(
        'models.Business',
        null=True,
        related_name='indicators',
    )
    year = fields.IntField(
        description='Год, к которому относятся показатели',
    )
    average_number_of_employees = fields.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        description='Среднесписочная численность персонала',
    )
    average_salary_of_employees = fields.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        description='Средняя заработная плата сотрудника',
    )
    taxes_to_the_budget = fields.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        description='Налоги, уплаченные в бюджет Москвы',
    )
    income_tax = fields.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        description='Налог на прибыль',
    )
    property_tax = fields.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        description='Налог на имущество',
    )
    land_tax = fields.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        description='Налог на землю',
    )
    personal_income_tax = fields.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        description='НДФЛ',
    )
    transport_tax = fields.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        description='Транспортный налог',
    )
    other_taxes = fields.DecimalField(
        max_digits=20,
        decimal_places=3,
        null=True,
        description='Прочие налоги',
    )
    created = fields.DatetimeField(
        auto_now_add=True,
        description='Дата создания бизнеса в БД',
    )

    def __str__(self):
        return f'{self.business}. Год - {self.year}'
