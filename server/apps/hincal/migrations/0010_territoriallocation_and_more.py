# Generated by Django 4.2.1 on 2023-05-26 13:00

from django.db import migrations, models
import django.db.models.deletion
import rules.contrib.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('hincal', '0009_remove_archive_average_salary_and_more'),
    ]

    operations = [
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
                        auto_now_add=True, verbose_name='Создан'
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='Изменен'),
                ),
                (
                    'shot_name',
                    models.CharField(
                        max_length=255, verbose_name='Короткое название'
                    ),
                ),
                (
                    'full_name',
                    models.CharField(
                        max_length=255, verbose_name='Полное название'
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
            ],
            options={
                'verbose_name': 'Территориальное расположение',
                'verbose_name_plural': 'Территориальное расположения',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.RemoveConstraint(
            model_name='business', name='territorial_location_valid',
        ),
        migrations.RemoveField(
            model_name='archive', name='avg_land_lease_costs',
        ),
        migrations.RemoveField(
            model_name='archive', name='avg_land_purchase_costs',
        ),
        migrations.RemoveField(
            model_name='archive', name='avg_property_lease_costs',
        ),
        migrations.RemoveField(
            model_name='archive', name='avg_property_purchase_costs',
        ),
        migrations.RemoveField(
            model_name='archive', name='avg_property_repair_costs',
        ),
        migrations.RemoveField(
            model_name='archive', name='land_cadastral_value',
        ),
        migrations.RemoveField(
            model_name='archive', name='property_cadastral_value',
        ),
        migrations.AddField(
            model_name='territoriallocation',
            name='tags',
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text='A comma-separated list of tags.',
                through='taggit.TaggedItem',
                to='taggit.Tag',
                verbose_name='Tags',
            ),
        ),
        migrations.AlterField(
            model_name='business',
            name='territorial_location',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='businesses',
                to='hincal.territoriallocation',
                verbose_name='Территориальное положение бизнеса',
            ),
        ),
    ]