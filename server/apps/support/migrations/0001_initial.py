# Generated by Django 4.2.1 on 2023-05-28 11:48

from django.db import migrations, models
import django.db.models.deletion
import rules.contrib.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('hincal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
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
                    models.ImageField(
                        blank=True,
                        upload_to='media',
                        verbose_name='Изображение',
                    ),
                ),
                (
                    'title',
                    models.CharField(max_length=255, verbose_name='Заголовок'),
                ),
                ('text', models.TextField(verbose_name='Полное описание меры')),
                (
                    'amount',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Сумма субсидий',
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
                    'extra_data',
                    models.JSONField(
                        blank=True,
                        null=True,
                        verbose_name='Дополнительные параметры',
                    ),
                ),
                (
                    'is_actual',
                    models.BooleanField(
                        default=False,
                        verbose_name='Является ли меря поддержки актуальной',
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
                'verbose_name': 'Мера поддержки бизнеса',
                'verbose_name_plural': 'Меры поддержки бизнеса',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Offer',
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
                    'title',
                    models.CharField(max_length=255, verbose_name='Заголовок'),
                ),
                (
                    'text',
                    models.TextField(
                        verbose_name='Полное описание предложения'
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
                    'interest_rate',
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name='Процентная ставка',
                    ),
                ),
                (
                    'loan_term',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Срок займа'
                    ),
                ),
                (
                    'amount',
                    models.CharField(
                        blank=True, max_length=255, verbose_name='Сумма займа'
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
                'verbose_name': 'Партнерское предложение',
                'verbose_name_plural': 'Партнерские предложения',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
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
