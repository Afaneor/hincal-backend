# Generated by Django 4.2.1 on 2023-05-28 11:48

from django.db import migrations, models
import rules.contrib.models
import server.apps.hincal.services.archive
import server.apps.hincal.services.validators
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Создан',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'year',
                    models.PositiveIntegerField(
                        default=2023,
                        verbose_name='Год, к которому относятся данные',
                    ),
                ),
                (
                    'income_tax_rate_to_the_subject_budget',
                    models.FloatField(
                        default=0.18,
                        verbose_name='Налог на прибыль, уплачиваемый в бюджет субъекта',
                    ),
                ),
                (
                    'income_tax_rate_to_the_federal_budget',
                    models.FloatField(
                        default=0.02,
                        verbose_name='Налог на прибыль, уплачиваемый в федеральный бюджет',
                    ),
                ),
                (
                    'land_tax_rate',
                    models.FloatField(
                        default=0.015,
                        verbose_name='Размер налоговой ставки на землю',
                    ),
                ),
                (
                    'property_tax_rate',
                    models.FloatField(
                        default=0.019,
                        verbose_name='Размер налоговой ставки на имущество',
                    ),
                ),
                (
                    'patent_tax_rate',
                    models.FloatField(
                        default=0.06,
                        verbose_name='Размер налоговой ставки по патенту',
                    ),
                ),
                (
                    'osn_tax_rate',
                    models.FloatField(
                        default=0.2,
                        verbose_name='Размер налоговой ставки по общей системе налогооблажения',
                    ),
                ),
                (
                    'ysn_tax_rate',
                    models.FloatField(
                        default=0.06,
                        verbose_name='Размер налоговой ставки по упрощенной системе налогооблажения',
                    ),
                ),
                (
                    'personal_income_rate',
                    models.FloatField(
                        default=0.013, verbose_name='Размер НДФЛ',
                    ),
                ),
                (
                    'pension_contributions_rate',
                    models.FloatField(
                        default=0.22,
                        verbose_name='Размер ставки для пенсионных отчислений',
                    ),
                ),
                (
                    'medical_contributions_rate',
                    models.FloatField(
                        default=0.051,
                        verbose_name='Размер ставки для медицинских отчислений',
                    ),
                ),
                (
                    'disability_contributions_rate',
                    models.FloatField(
                        default=0.029,
                        verbose_name='Размер ставки для по нетрудоспособности',
                    ),
                ),
                (
                    'lower_tax_margin_error',
                    models.FloatField(
                        default=0.85,
                        verbose_name='Нижний уровень погрешности для поиска записей по налогам',
                    ),
                ),
                (
                    'upper_tax_margin_error',
                    models.FloatField(
                        default=1.15,
                        verbose_name='Верхний уровень погрешности для поиска записей по налогам',
                    ),
                ),
                (
                    'cost_accounting',
                    models.JSONField(
                        default=server.apps.hincal.services.archive.get_cost_accounting,
                        verbose_name='Стоимость услуг на ведение бухгалтерского учета',
                    ),
                ),
                (
                    'registration_costs',
                    models.JSONField(
                        default=server.apps.hincal.services.archive.get_registration_costs,
                        verbose_name='Расходы на регистрацию бизнеса',
                    ),
                ),
                (
                    'avg_land_cadastral_value',
                    models.FloatField(
                        default=17.23389,
                        verbose_name='Средняя кадастровая стоимость на землю, тыс. руб.',
                    ),
                ),
                (
                    'avg_land_lease_costs',
                    models.FloatField(
                        default=60,
                        verbose_name='Средняя стоимость на аренду земли, тыс. руб.',
                    ),
                ),
                (
                    'avg_land_purchase_costs',
                    models.FloatField(
                        default=100,
                        verbose_name='Средняя стоимость на покупку земли, тыс. руб.',
                    ),
                ),
                (
                    'avg_property_cadastral_value',
                    models.FloatField(
                        default=17.23389,
                        verbose_name='Средняя кадастровая стоимость на имуществу, тыс. руб.',
                    ),
                ),
                (
                    'avg_property_lease_costs',
                    models.FloatField(
                        default=100,
                        verbose_name='Средняя стоимость на аренду имущества, тыс. руб.',
                    ),
                ),
                (
                    'avg_property_purchase_costs',
                    models.FloatField(
                        default=200,
                        verbose_name='Средняя стоимость на покупку  имуществу, тыс. руб.',
                    ),
                ),
                (
                    'avg_capital_construction_costs',
                    models.FloatField(
                        default=100,
                        verbose_name='Затраты на капитальное строительство, тыс. руб.',
                    ),
                ),
                (
                    'is_actual',
                    models.BooleanField(
                        default=True,
                        verbose_name='Актуальные данные в архиве или нет',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Архив',
                'verbose_name_plural': 'Архивы',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Создан',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'position',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Должность пользователя в бизнесе',
                    ),
                ),
                (
                    'type',
                    models.CharField(
                        blank=True,
                        choices=[
                            ('legal', 'Юридическое лицо'),
                            ('individual', 'Индивидуальный предприниматель'),
                            ('physical', 'Физическое лицо'),
                        ],
                        max_length=255,
                        verbose_name='Тип бизнеса',
                    ),
                ),
                (
                    'inn',
                    models.CharField(
                        blank=True,
                        max_length=12,
                        validators=[
                            server.apps.hincal.services.validators.inn_validator
                        ],
                        verbose_name='ИНН физического лица, ИП или компания',
                    ),
                ),
                (
                    'hid',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Уникальный id контрагента в dadata',
                    ),
                ),
                (
                    'short_business_name',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Короткое название ИП или компании',
                    ),
                ),
                (
                    'full_business_name',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Полное название ИП или компании',
                    ),
                ),
                (
                    'management_name',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='ФИО руководителя, только для компании',
                    ),
                ),
                (
                    'management_position',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Должность руководителя, только для компании',
                    ),
                ),
                (
                    'full_opf',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Полное наименование правовой формы',
                    ),
                ),
                (
                    'short_opf',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Короткое наименование правовой формы',
                    ),
                ),
                (
                    'okved',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='ОКВЕД',
                    ),
                ),
                (
                    'first_name',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Имя',
                    ),
                ),
                (
                    'last_name',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Фамилия',
                    ),
                ),
                (
                    'middle_name',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Отчество',
                    ),
                ),
                (
                    'address',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Полный адрес',
                    ),
                ),
                (
                    'country',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Страна',
                    ),
                ),
                (
                    'region',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Город',
                    ),
                ),
                (
                    'city_area',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Область, округ',
                    ),
                ),
                (
                    'city_district',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Район',
                    ),
                ),
                (
                    'phone',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Телефон, относящийся к бизнесу',
                    ),
                ),
                (
                    'email',
                    models.EmailField(
                        blank=True,
                        max_length=255,
                        verbose_name='Email, относящийся к бизнесу',
                    ),
                ),
                (
                    'site',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Сайт, относящийся к бизнесу',
                    ),
                ),
                (
                    'type_tax_system',
                    models.CharField(
                        choices=[
                            ('osn', 'Общая'),
                            ('ysn', 'Упрощенная'),
                            ('patent', 'Патентная'),
                        ],
                        default='osn',
                        max_length=255,
                        verbose_name='Тип системы налогооблажения',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Бизнес',
                'verbose_name_plural': 'Бизнесы',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BusinessIndicator',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Создан',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'year',
                    models.IntegerField(
                        verbose_name='Год, к которому относятся показатели',
                    ),
                ),
                (
                    'average_number_of_staff',
                    models.FloatField(
                        null=True,
                        verbose_name='Среднесписочная численность сотрудников',
                    ),
                ),
                (
                    'average_salary_of_staff',
                    models.FloatField(
                        null=True,
                        verbose_name='Средняя заработная плата сотрудника',
                    ),
                ),
                (
                    'taxes_to_the_budget',
                    models.FloatField(
                        null=True,
                        verbose_name='Налоги, уплаченные в бюджет Москвы',
                    ),
                ),
                (
                    'income_tax',
                    models.FloatField(
                        null=True, verbose_name='Налог на прибыль',
                    ),
                ),
                (
                    'property_tax',
                    models.FloatField(
                        null=True, verbose_name='Налог на имущество',
                    ),
                ),
                (
                    'land_tax',
                    models.FloatField(null=True, verbose_name='Налог на землю'),
                ),
                (
                    'personal_income_tax',
                    models.FloatField(null=True, verbose_name='НДФЛ'),
                ),
                (
                    'transport_tax',
                    models.FloatField(
                        null=True, verbose_name='Транспортный налог',
                    ),
                ),
                (
                    'other_taxes',
                    models.FloatField(null=True, verbose_name='Прочие налоги'),
                ),
            ],
            options={
                'verbose_name': 'Индикатор бизнеса',
                'verbose_name_plural': 'Индикаторы бизнесов',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Создан',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'name',
                    models.CharField(
                        unique=True, verbose_name='Название оборудования',
                    ),
                ),
                (
                    'cost',
                    models.FloatField(verbose_name='Стоимость оборудования'),
                ),
            ],
            options={
                'verbose_name': 'Оборудование',
                'verbose_name_plural': 'Оборудования',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SubSector',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Создан',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=255, unique=True, verbose_name='Название',
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        max_length=255,
                        unique=True,
                        verbose_name='Название на английском языке',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Подотрасль',
                'verbose_name_plural': 'Подотрасли',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TerritorialLocation',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Создан',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'shot_name',
                    models.CharField(
                        max_length=255, verbose_name='Короткое название',
                    ),
                ),
                (
                    'full_name',
                    models.CharField(
                        max_length=255, verbose_name='Полное название',
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        max_length=255,
                        unique=True,
                        verbose_name='Название на английском языке',
                    ),
                ),
                (
                    'avg_land_cadastral_value',
                    models.FloatField(
                        default=18.23389,
                        verbose_name='Средняя кадастровая стоимость на землю, тыс. руб.',
                    ),
                ),
                (
                    'avg_land_lease_costs',
                    models.FloatField(
                        default=1.432,
                        verbose_name='Средняя стоимость на аренду земли, тыс. руб.',
                    ),
                ),
                (
                    'avg_land_purchase_costs',
                    models.FloatField(
                        default=91.4233,
                        verbose_name='Средняя стоимость на покупку земли, тыс. руб.',
                    ),
                ),
                (
                    'avg_property_cadastral_value',
                    models.FloatField(
                        default=57.23389,
                        verbose_name='Средняя кадастровая стоимость на имуществу, тыс. руб.',
                    ),
                ),
                (
                    'avg_property_lease_costs',
                    models.FloatField(
                        default=2.6314,
                        verbose_name='Средняя стоимость на аренду имущества, тыс. руб.',
                    ),
                ),
                (
                    'avg_property_purchase_costs',
                    models.FloatField(
                        default=252.231,
                        verbose_name='Средняя стоимость на покупку  имуществу, тыс. руб.',
                    ),
                ),
                (
                    'extra_data',
                    models.JSONField(
                        blank=True,
                        null=True,
                        verbose_name='Дополнительные параметры',
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text='A comma-separated list of tags.',
                        through='taggit.TaggedItem',
                        to='taggit.Tag',
                        verbose_name='Tags',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Территориальное расположение',
                'verbose_name_plural': 'Территориальное расположения',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Создан',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=255, unique=True, verbose_name='Название',
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        max_length=255,
                        unique=True,
                        verbose_name='Название на английском языке',
                    ),
                ),
                (
                    'possible_income_from_patent',
                    models.JSONField(
                        default=server.apps.hincal.services.archive.get_possible_income_from_patent,
                        verbose_name='Возможный доход по патентной системе налогообложения, тыс. руб.',
                    ),
                ),
                (
                    'possible_income_on_market',
                    models.JSONField(
                        default=server.apps.hincal.services.archive.get_possible_income_on_market,
                        verbose_name='Возможный доход, тыс. руб.',
                    ),
                ),
                (
                    'average_salary_of_staff',
                    models.JSONField(
                        default=server.apps.hincal.services.archive.get_average_salary_of_staff,
                        verbose_name='Средняя заработная плата сотрудника, тыс. руб.',
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text='A comma-separated list of tags.',
                        through='taggit.TaggedItem',
                        to='taggit.Tag',
                        verbose_name='Tags',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Отрасль',
                'verbose_name_plural': 'Отрасли',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True, verbose_name='Создан',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'initial_data',
                    models.JSONField(
                        null=True,
                        verbose_name='Исходные данные по которым был сформирован отчет',
                    ),
                ),
                (
                    'context',
                    models.JSONField(
                        null=True, verbose_name='Данные для формирования отчета',
                    ),
                ),
                (
                    'total_investment_amount_bi',
                    models.FloatField(
                        null=True,
                        verbose_name='Общая сумма инвестирований из БД',
                    ),
                ),
                (
                    'total_investment_amount_math',
                    models.FloatField(
                        null=True,
                        verbose_name='Общая сумма инвестирований, рассчитанная математически',
                    ),
                ),
                (
                    'sector',
                    models.ForeignKey(
                        null=True,
                        on_delete=models.deletion.CASCADE,
                        related_name='reports',
                        to='hincal.sector',
                        verbose_name='Отрасль хозяйственной деятельности',
                    ),
                ),
                (
                    'tags',
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text='A comma-separated list of tags.',
                        through='taggit.TaggedItem',
                        to='taggit.Tag',
                        verbose_name='Tags',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Отчет',
                'verbose_name_plural': 'Отчеты',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
    ]
