# Generated by Django 4.2.1 on 2023-05-25 18:27

from django.db import migrations, models
import server.apps.hincal.services.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hincal', '0004_remove_business_sector_valid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='inn',
            field=models.CharField(
                blank=True,
                max_length=12,
                validators=[
                    server.apps.hincal.services.validators.inn_validator
                ],
                verbose_name='ИНН физического лица, ИП или компания',
            ),
        ),
        migrations.AlterField(
            model_name='business',
            name='sub_sector',
            field=models.CharField(
                blank=True,
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
                    ('other', 'Иные подсектора'),
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
    ]
