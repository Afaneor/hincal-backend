# Generated by Django 4.2.1 on 2023-05-27 08:07

from django.db import migrations, models
import django.db.models.deletion
import rules.contrib.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('hincal', '0014_archive_avg_land_lease_costs_and_more'),
        ('support', '0002_offer_amount_offer_interest_rate_offer_loan_term'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
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
                    'preview_image',
                    models.CharField(blank=True, verbose_name='Изображение'),
                ),
                (
                    'title',
                    models.CharField(max_length=255, verbose_name='Заголовок'),
                ),
                (
                    'text',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Краткое описание объекта',
                    ),
                ),
                (
                    'address',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Адрес площадки',
                    ),
                ),
                (
                    'site',
                    models.URLField(
                        blank=True,
                        verbose_name='Ссылка на сторонний ресурс с подробной информацией',
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
                (
                    'territorial_location',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='areas',
                        to='hincal.territoriallocation',
                        verbose_name='Территориальное положение площадки',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Площадка для осуществления деятельности',
                'verbose_name_plural': 'Площадки для осуществления деятельности',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
    ]
