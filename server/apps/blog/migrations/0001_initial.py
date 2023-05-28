# Generated by Django 4.2.1 on 2023-05-25 07:19

from django.db import migrations, models
import rules.contrib.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
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
                (
                    'text',
                    models.TextField(verbose_name='Полное описание новости'),
                ),
                (
                    'is_published',
                    models.BooleanField(
                        default=False,
                        verbose_name='Пост доступен для просмотра',
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
                'verbose_name': 'Запись в блоге',
                'verbose_name_plural': 'Записи в блоге',
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(rules.contrib.models.RulesModelMixin, models.Model),
        ),
    ]
