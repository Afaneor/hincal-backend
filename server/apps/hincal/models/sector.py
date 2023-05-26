from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from server.apps.services.base_model import AbstractBaseModel


class Sector(AbstractBaseModel):
    """Отрасль."""

    name = models.CharField(
        _('Название'),
        max_length=settings.MAX_STRING_LENGTH,
        unique=True,
    )
    slug = models.SlugField(
        _('Название на английском языке'),
        max_length=settings.MAX_STRING_LENGTH,
        unique=True,
    )
    possible_income_from_patent = models.PositiveIntegerField(
        _('Возможный доход по патентной системе налогообложения, тыс. руб.'),
        default=10000,
    )
    avg_salary_of_staff = models.FloatField(
        _('Средняя заработная плата сотрудника, тыс. руб.'),
        default=100,
    )
    tags = TaggableManager(blank=True)

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Отрасль')
        verbose_name_plural = _('Отрасли')

    def __str__(self):
        return self.name
