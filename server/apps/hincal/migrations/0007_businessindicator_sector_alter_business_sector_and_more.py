# Generated by Django 4.2.1 on 2023-05-26 06:54

from django.db import migrations, models
import django.db.models.deletion
import rules.contrib.models


class Migration(migrations.Migration):

    dependencies = [
        ('hincal', '0006_remove_business_sub_sector_valid_and_more'),
    ]

    operations = [
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
                        max_length=255, unique=True, verbose_name='Название'
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
                'verbose_name': 'Сектор',
                'verbose_name_plural': 'Секторы',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.AlterField(
            model_name='business',
            name='sector',
            field=models.CharField(
                choices=[
                    ('food_industry', 'Пищевая промышленность'),
                    (
                        'radio_electronics_and_instrumentation',
                        'Радиоэлектроника и приборостроение',
                    ),
                    ('aviation_industry', 'Авиационная промышленность'),
                    ('automotive_industry', 'Автомобильная промышленность'),
                    ('general_mechanical_engineering', 'Общее машиностроение'),
                    ('light_industry', 'Легкая промышленность'),
                    (
                        'production_of_petroleum_products',
                        'Производство кокса и нефтепродуктов',
                    ),
                    ('chemical_industry', 'Химическая промышленность'),
                    (
                        'production_of_building_materials',
                        'Производство строительных материалов',
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
                    ('printing_activity', 'Полиграфическая деятельность'),
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
                    ('other', 'Иные сектора'),
                ],
                max_length=255,
                verbose_name='Отрасль хозяйственной деятельности',
            ),
        ),
        migrations.DeleteModel(name='Indicator',),
        migrations.AddField(
            model_name='businessindicator',
            name='business',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='business_indicators',
                to='hincal.business',
                verbose_name='Бизнес',
            ),
        ),
        migrations.AddConstraint(
            model_name='businessindicator',
            constraint=models.UniqueConstraint(
                fields=('year', 'business'), name='unique_year_for_business'
            ),
        ),
    ]
