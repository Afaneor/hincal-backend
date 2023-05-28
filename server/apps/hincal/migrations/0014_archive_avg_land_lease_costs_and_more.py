# Generated by Django 4.2.1 on 2023-05-26 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hincal', '0013_archive_disability_contributions_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='archive',
            name='avg_land_lease_costs',
            field=models.FloatField(
                default=60,
                verbose_name='Средняя стоимость на аренду земли, тыс. руб.',
            ),
        ),
        migrations.AddField(
            model_name='archive',
            name='avg_land_purchase_costs',
            field=models.FloatField(
                default=100,
                verbose_name='Средняя стоимость на покупку земли, тыс. руб.',
            ),
        ),
        migrations.AddField(
            model_name='archive',
            name='avg_property_lease_costs',
            field=models.FloatField(
                default=100,
                verbose_name='Средняя стоимость на аренду имущества, тыс. руб.',
            ),
        ),
        migrations.AddField(
            model_name='archive',
            name='avg_property_purchase_costs',
            field=models.FloatField(
                default=200,
                verbose_name='Средняя стоимость на покупку  имуществу, тыс. руб.',
            ),
        ),
    ]