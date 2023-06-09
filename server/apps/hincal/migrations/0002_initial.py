# Generated by Django 4.2.1 on 2023-05-28 11:48

from django.conf import settings
from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('hincal', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name='reports',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Пользователь',
            ),
        ),
        migrations.AddField(
            model_name='equipment',
            name='tags',
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text='A comma-separated list of tags.',
                through='taggit.TaggedItem',
                to='taggit.Tag',
                verbose_name='Tags',
            ),
        ),
        migrations.AddField(
            model_name='businessindicator',
            name='business',
            field=models.ForeignKey(
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name='business_indicators',
                to='hincal.business',
                verbose_name='Бизнес',
            ),
        ),
        migrations.AddField(
            model_name='business',
            name='sector',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name='businesses',
                to='hincal.sector',
                verbose_name='Отрасль хозяйственной деятельности',
            ),
        ),
        migrations.AddField(
            model_name='business',
            name='sub_sector',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name='business',
                to='hincal.subsector',
                verbose_name='Подотрасль хозяйственной деятельности',
            ),
        ),
        migrations.AddField(
            model_name='business',
            name='territorial_location',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name='businesses',
                to='hincal.territoriallocation',
                verbose_name='Территориальное положение бизнеса',
            ),
        ),
        migrations.AddField(
            model_name='business',
            name='user',
            field=models.ForeignKey(
                null=True,
                on_delete=models.deletion.CASCADE,
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
            model_name='businessindicator',
            constraint=models.UniqueConstraint(
                fields=('year', 'business'), name='unique_year_for_business',
            ),
        ),
        migrations.AddConstraint(
            model_name='business',
            constraint=models.CheckConstraint(
                check=models.Q(
                    ('type__in', ['legal', 'individual', 'physical', '']),
                ),
                name='type_valid',
            ),
        ),
        migrations.AddConstraint(
            model_name='business',
            constraint=models.CheckConstraint(
                check=models.Q(
                    ('type_tax_system__in', ['osn', 'ysn', 'patent']),
                ),
                name='type_tax_system_valid',
            ),
        ),
    ]
