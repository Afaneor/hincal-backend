# Generated by Django 4.2.1 on 2023-05-25 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hincal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic',
            name='user',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='statistics',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Пользователь',
            ),
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='reports',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Пользователь',
            ),
        ),
        migrations.AddField(
            model_name='indicator',
            name='business',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='indicators',
                to='hincal.business',
                verbose_name='Бизнес',
            ),
        ),
        migrations.AddField(
            model_name='business',
            name='user',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='businesses',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Пользователь',
            ),
        ),
        migrations.AddConstraint(
            model_name='archive',
            constraint=models.UniqueConstraint(
                condition=models.Q(('is_actual', True)),
                fields=('is_actual',),
                name='unique_is_actual_for_archive',
            ),
        ),
        migrations.AddConstraint(
            model_name='indicator',
            constraint=models.UniqueConstraint(
                fields=('year', 'business'), name='unique_year_for_business'
            ),
        ),
        migrations.AddConstraint(
            model_name='business',
            constraint=models.CheckConstraint(
                check=models.Q(
                    ('type__in', ['legal', 'individual', 'physical', ''])
                ),
                name='type_valid',
            ),
        ),
        migrations.AddConstraint(
            model_name='business',
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        'sector__in',
                        [
                            'food_industry',
                            'radio_electronics_and_instrumentation',
                            'aviation_industry',
                            'automotive_industry',
                            'general_mechanical_engineering',
                            'light_industry',
                            'production_of_petroleum_products',
                            'chemical_industry',
                            'production_of_building_materials',
                            'production_for_military',
                            'pharmaceutical_industry',
                            'fuel_and_energy_complex',
                            'medical_industry',
                            'cable_industry',
                            'woodworking',
                            'metallurgy_and_metalworking',
                            'printing_activity',
                            'production_of_other_consumer_goods',
                            'beverage_production',
                            'scientific_activity',
                            'machine_tool_industry',
                            'shipbuilding',
                            'production_of_railway_transport',
                            'manufacture_of_consumer_electronics',
                            'additive_technologies',
                        ],
                    )
                ),
                name='sector_valid',
            ),
        ),
        migrations.AddConstraint(
            model_name='business',
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        'sub_sector__in',
                        [
                            'dairy_industry',
                            'instrumentation',
                            'meat_industry',
                            'confectionery_industry',
                            'manufacture_of_other_general',
                            'bakery_industry',
                            'production_of_railway_transport',
                            'fishing_industry',
                            'production_of_general_purpose_equipment',
                            'production_of_canned_fruits_and_vegetables',
                            'electrical_engineering',
                            'production_of_other_special_purpose_machines',
                            'machine_tool_industry',
                            'microelectronics',
                            'milling_and_cereal_industry',
                            'other_industries',
                            'beverage_production',
                            'animal_feed',
                            'electrical_engineering_and_shipbuilding',
                            'sugar_industry',
                            'production_of_equipment_for_agriculture_and_forestry',
                            'fat_and_oil_industry',
                            'metalworking',
                        ],
                    )
                ),
                name='sub_sector_valid',
            ),
        ),
        migrations.AddConstraint(
            model_name='business',
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        'territorial_location__in',
                        [
                            'wao',
                            'zao',
                            'zelao',
                            'nao',
                            'sao',
                            'swao',
                            'szao',
                            'tao',
                            'cao',
                            'yuao',
                            'yuwao',
                            'yuzao',
                            'other',
                            '',
                        ],
                    )
                ),
                name='territorial_location_valid',
            ),
        ),
    ]