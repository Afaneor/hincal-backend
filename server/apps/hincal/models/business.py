from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.hincal.services.enums import (
    BusinessSector,
    BusinessSubSector,
    TerritorialLocation,
    TypeBusiness,
)
from server.apps.services.base_model import AbstractBaseModel


class Business(AbstractBaseModel):
    """Бизнес.

    Компании и ИП получаются из DaData.
    Физическое лицо заполняет данные руками.
    """
    
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='businesses',
        db_index=True,
        null=True,
    )
    position = models.CharField(
        _('Должность пользователя в бизнесе'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,

    )
    type = models.CharField(
        _('Тип бизнеса'),
        max_length=settings.MAX_STRING_LENGTH,
        choices=TypeBusiness.choices,
        blank=True,
    )
    inn = models.CharField(
        _('ИНН физического лица, ИП или компания'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    sector = models.CharField(
        _('Отрасль хозяйственной деятельности'),
        max_length=settings.MAX_STRING_LENGTH,
        choices=BusinessSector.choices,
    )
    sub_sector = models.CharField(
        _('Подотрасль хозяйственной деятельности'),
        max_length=settings.MAX_STRING_LENGTH,
        choices=BusinessSubSector.choices,
    )
    territorial_location = models.CharField(
        _('Территориальное положение бизнеса'),
        max_length=settings.MAX_STRING_LENGTH,
        choices=TerritorialLocation.choices,
        blank=True,
    )
    # Основная информация по бизнесу.
    hid = models.CharField(
        _('Уникальный id контрагента в dadata'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    short_business_name = models.CharField(
        _('Короткое название ИП или компании'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    full_business_name = models.CharField(
        _('Полное название ИП или компании'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    management_name = models.CharField(
        _('ФИО руководителя, только для компании'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    management_position = models.CharField(
        _('Должность руководителя, только для компании'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    full_opf = models.CharField(
        _('Полное наименование правовой формы'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    short_opf = models.CharField(
        _('Короткое наименование правовой формы'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    okved = models.CharField(
        _('ОКВЕД'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    # Если ИП, то будет ФИО
    first_name = models.CharField(
        _('Имя'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    middle_name = models.CharField(
        _('Отчество'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    # Данные по адресу.
    address = models.CharField(
        _('Полный адрес'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    country = models.CharField(
        _('Страна'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    region = models.CharField(
        _('Город'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    city_area = models.CharField(
        _('Область, округ'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    city_district = models.CharField(
        _('Район'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    # Контактная информация.
    phone = models.CharField(
        _('Телефон, относящийся к бизнесу'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    email = models.EmailField(
        _('Email, относящийся к бизнесу'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )
    site = models.CharField(
        _('Сайт, относящийся к бизнесу'),
        max_length=settings.MAX_STRING_LENGTH,
        blank=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Бизнес')
        verbose_name_plural = _('Бизнесы')
        constraints = [
            models.CheckConstraint(
                name='type_valid',
                check=models.Q(type__in=[*TypeBusiness.values, '']),
            ),
            models.CheckConstraint(
                name='sector_valid',
                check=models.Q(sector__in=BusinessSector.values),
            ),
            models.CheckConstraint(
                name='sub_sector_valid',
                check=models.Q(sub_sector__in=BusinessSubSector.values),
            ),
            models.CheckConstraint(
                name='territorial_location_valid',
                check=models.Q(
                    territorial_location__in=[*TerritorialLocation.values, '']
                ),
            ),
        ]

    def __str__(self):
        return f'{self.type} - {self.user}. ИНН - {self.inn}'
