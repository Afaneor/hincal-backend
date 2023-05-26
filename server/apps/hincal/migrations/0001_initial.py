# Generated by Django 4.2.1 on 2023-05-25 07:19

from django.db import migrations, models
import rules.contrib.models
import server.apps.hincal.services.archive


class Migration(migrations.Migration):

    initial = True

    dependencies = []

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
                        auto_now_add=True, verbose_name='Создан'
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'year',
                    models.PositiveIntegerField(
                        verbose_name='Год, к которому относятся данные'
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
                        verbose_name='Размер налогаовой ставки на имущество',
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
                    'personal_income_rate',
                    models.FloatField(
                        default=0.013, verbose_name='Размер НДФЛ'
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
                    'lower_tax_margin_error',
                    models.FloatField(
                        default=0.9,
                        verbose_name='Нижний уровень погрешности для поиска записей по налогам',
                    ),
                ),
                (
                    'upper_tax_margin_error',
                    models.FloatField(
                        default=1.1,
                        verbose_name='Верхний уровень погрешности для поиска записей по налогам',
                    ),
                ),
                (
                    'land_cadastral_value',
                    models.JSONField(
                        default=server.apps.hincal.services.archive.get_land_cadastral_value,
                        verbose_name='Кадастровая стоимость земли',
                    ),
                ),
                (
                    'property_cadastral_value',
                    models.JSONField(
                        default=server.apps.hincal.services.archive.get_property_cadastral_value,
                        verbose_name='Кадастровая стоимость имущества',
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
                    'possible_income_from_patent',
                    models.JSONField(
                        default={},
                        verbose_name='Возможный доход для ИП по патентной системе',
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
                    'avg_land_lease_costs',
                    models.FloatField(
                        default=50,
                        verbose_name='Средняя стоимость аренды земли',
                    ),
                ),
                (
                    'avg_land_purchase_costs',
                    models.FloatField(
                        default=100,
                        verbose_name='Средняя стоимость покупки земли',
                    ),
                ),
                (
                    'avg_property_lease_costs',
                    models.FloatField(
                        default=100,
                        verbose_name='Средняя стоимость аренды недвижимости',
                    ),
                ),
                (
                    'avg_property_purchase_costs',
                    models.FloatField(
                        default=200,
                        verbose_name='Средняя стоимость покупки недвижимости',
                    ),
                ),
                (
                    'avg_property_repair_costs',
                    models.FloatField(
                        default=100,
                        verbose_name='Средняя стоимость капитального строительства недвижимости',
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
                        auto_now_add=True, verbose_name='Создан'
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
                        max_length=255,
                        verbose_name='ИНН физического лица, ИП или компания',
                    ),
                ),
                (
                    'sector',
                    models.CharField(
                        choices=[
                            ('food_industry', 'Пищевая промышленность'),
                            (
                                'radio_electronics_and_instrumentation',
                                'Радиоэлектроника и приборостроение',
                            ),
                            ('aviation_industry', 'Авиационная промышленность'),
                            (
                                'automotive_industry',
                                'Автомобильная промышленность',
                            ),
                            (
                                'general_mechanical_engineering',
                                'Общее машиностроение',
                            ),
                            ('light_industry', 'Легкая промышленность'),
                            (
                                'production_of_petroleum_products',
                                'Производство кокса и нефтепродуктов',
                            ),
                            ('chemical_industry', 'Химическая промышленность'),
                            (
                                'production_of_building_materials',
                                'Химическая промышленность',
                            ),
                            (
                                'production_for_military',
                                'Производство оружия, боеприпасов, спецхимии, военных машин',
                            ),
                            (
                                'pharmaceutical_industry',
                                'Фармацевтическая промышленность',
                            ),
                            (
                                'fuel_and_energy_complex',
                                'Топливно-энергетический комплекс',
                            ),
                            ('medical_industry', 'Медицинская промышленность'),
                            ('cable_industry', 'Кабельная промышленность'),
                            ('woodworking', 'Деревообрабатывающая'),
                            (
                                'metallurgy_and_metalworking',
                                'Металлургия и металлообработка',
                            ),
                            (
                                'printing_activity',
                                'Полиграфическая деятельность',
                            ),
                            (
                                'production_of_other_consumer_goods',
                                'Производство прочих товаров народного потребления',
                            ),
                            ('beverage_production', 'Производство напитков'),
                            ('scientific_activity', 'Научная деятельность'),
                            (
                                'machine_tool_industry',
                                'Станкоинструментальная промышленность',
                            ),
                            ('shipbuilding', 'Судостроение'),
                            (
                                'production_of_railway_transport',
                                'Производство ж/д транспорта',
                            ),
                            (
                                'manufacture_of_consumer_electronics',
                                'Производство бытовой электроники и электрических приборов',
                            ),
                            ('additive_technologies', 'Аддитивные технологии'),
                        ],
                        max_length=255,
                        verbose_name='Отрасль хозяйственной деятельности',
                    ),
                ),
                (
                    'sub_sector',
                    models.CharField(
                        choices=[
                            ('dairy_industry', 'Молочная отрасль'),
                            ('instrumentation', 'Приборостроение'),
                            ('meat_industry', 'Мясная отрасль'),
                            ('confectionery_industry', 'Кондитерская отрасль'),
                            (
                                'manufacture_of_other_general',
                                'Производство прочих машин и оборудования общего назначения',
                            ),
                            ('bakery_industry', 'Хлебопекарная отрасль'),
                            (
                                'production_of_railway_transport',
                                'Производство ж/д транспорта',
                            ),
                            ('fishing_industry', 'Рыбная отрасль'),
                            (
                                'production_of_general_purpose_equipment',
                                'Производство машин и оборудования общего назначения',
                            ),
                            (
                                'production_of_canned_fruits_and_vegetables',
                                'Производство плодоовощных консервов',
                            ),
                            ('electrical_engineering', 'Электротехника'),
                            (
                                'production_of_other_special_purpose_machines',
                                'Производство прочих машин специального назначения',
                            ),
                            (
                                'machine_tool_industry',
                                'Станкоинструментальная промышленность',
                            ),
                            ('microelectronics', 'Микроэлектроника'),
                            (
                                'milling_and_cereal_industry',
                                'Мукомольно-крупяная отрасль',
                            ),
                            ('other_industries', 'Иные отрасли'),
                            ('beverage_production', 'Производство напитков'),
                            ('animal_feed', 'Корма для животных'),
                            (
                                'electrical_engineering_and_shipbuilding',
                                'Электротехника/Судостроение',
                            ),
                            ('sugar_industry', 'Сахарная отрасль'),
                            (
                                'production_of_equipment_for_agriculture_and_forestry',
                                'Производство машин и оборудования для сельского и лесного хозяйства',
                            ),
                            ('fat_and_oil_industry', 'Масложировая отрасль'),
                            ('metalworking', 'Металлообработка'),
                        ],
                        max_length=255,
                        verbose_name='Подотрасль хозяйственной деятельности',
                    ),
                ),
                (
                    'territorial_location',
                    models.CharField(
                        blank=True,
                        choices=[
                            ('wao', 'ВАО'),
                            ('zao', 'ЗАО'),
                            ('zelao', 'ЗелАО'),
                            ('nao', 'НАО'),
                            ('sao', 'САО'),
                            ('swao', 'СВАО'),
                            ('szao', 'СЗАО'),
                            ('tao', 'ТАО'),
                            ('cao', 'ЦАО'),
                            ('yuao', 'ЮАО'),
                            ('yuwao', 'ЮВАО'),
                            ('yuzao', 'ЮЗАО'),
                            ('other', 'Другое'),
                        ],
                        max_length=255,
                        verbose_name='Территориальное положение бизнеса',
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
                        blank=True, max_length=255, verbose_name='ОКВЕД'
                    ),
                ),
                (
                    'first_name',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Имя'
                    ),
                ),
                (
                    'last_name',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Фамилия'
                    ),
                ),
                (
                    'middle_name',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Отчество'
                    ),
                ),
                (
                    'address',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Полный адрес'
                    ),
                ),
                (
                    'country',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Страна'
                    ),
                ),
                (
                    'region',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Город'
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
                        blank=True, max_length=255, verbose_name='Район'
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
                        auto_now_add=True, verbose_name='Создан'
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'name',
                    models.CharField(
                        unique=True, verbose_name='Название оборудования'
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
            name='Indicator',
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
                        auto_now_add=True, verbose_name='Создан'
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'year',
                    models.IntegerField(
                        verbose_name='Год, к которому относятся показатели'
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
                        null=True, verbose_name='Налог на прибыль'
                    ),
                ),
                (
                    'property_tax',
                    models.FloatField(
                        null=True, verbose_name='Налог на имущество'
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
                        null=True, verbose_name='Транспортный налог'
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
                        auto_now_add=True, verbose_name='Создан'
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'initial_data',
                    models.JSONField(
                        verbose_name='Исходные данные по которым был сформирован отчет'
                    ),
                ),
                (
                    'context',
                    models.JSONField(
                        verbose_name='Данные для формирования отчета'
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
        migrations.CreateModel(
            name='Statistic',
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
                        auto_now_add=True, verbose_name='Создан'
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'popular_sector',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Популярная отрасль для инвестирования',
                    ),
                ),
                (
                    'average_investment_amount',
                    models.FloatField(
                        null=True, verbose_name='Средняя сумма инвестирования'
                    ),
                ),
                (
                    'total_investment_amount',
                    models.FloatField(
                        null=True, verbose_name='Общая сумма инвестирования'
                    ),
                ),
                (
                    'amount_of_use_of_the_calculator',
                    models.PositiveIntegerField(
                        default=0,
                        verbose_name='Сколько раз использовался калькулятор',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Статистика',
                'verbose_name_plural': 'Статистика',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
    ]
