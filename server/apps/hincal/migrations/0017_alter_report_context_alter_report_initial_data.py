# Generated by Django 4.2.1 on 2023-05-28 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hincal', '0016_archive_avg_capital_construction_costs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='context',
            field=models.JSONField(
                null=True, verbose_name='Данные для формирования отчета'
            ),
        ),
        migrations.AlterField(
            model_name='report',
            name='initial_data',
            field=models.JSONField(
                null=True,
                verbose_name='Исходные данные по которым был сформирован отчет',
            ),
        ),
    ]