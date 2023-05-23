from enum import Enum

from tortoise import models, fields

from app import config


class TypeBusiness(str, Enum):
    """Тип бизнеса: ИП или компания."""

    LEGAL = 'legal'
    INDIVIDUAL = 'individual'
    PHYSICAL = 'physical'


class SectorBusiness(str, Enum):
    """Отрасль хозяйственной деятельности"""

    LEGAL = 'legal'
    INDIVIDUAL = 'individual'


class Business(models.Model):
    """Бизнес.

    Компании и ИП получаются из DaData.
    Физическое лицо заполняет данные руками.
    """

    id = fields.IntField(pk=True)
    account = fields.ForeignKeyField(
        'models.User',
        null=True,
        related_name='businesses',
    )
    sector = fields.CharEnumField(
        enum_type=SectorBusiness,
        null=True,
        description='Отрасль хозяйственной деятельности',
    )
    sub_sector = fields.CharEnumField(
        enum_type=SectorBusiness,
        null=True,
        description='Подотрасль хозяйственной деятельности',
    )
    inn = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=False,
        description='ИНН физического лица, ИП или компания',
    )
    position = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Должность пользователя в бизнесе',
    )
    type = fields.CharEnumField(
        enum_type=TypeBusiness,
        null=True,
        description='Тип бизнеса: физическое лицо, ИП или компания.',
    )
    hid = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Уникальный id контрагента в dadata',
    )

    # Основная информация по бизнесу.
    short_business_name = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Короткое название ИП или компании',
    )
    full_business_name = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Полное название ИП или компании',
    )
    management_name = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='ФИО руководителя, только для компании',
    )
    management_position = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Должность руководителя, только для компании',
    )
    full_opf = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Полное наименование правовой формы',
    )
    short_opf = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Короткое наименование правовой формы',
    )
    okved = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='ОКВЕД',
    )

    # Если ИП, то будет ФИО
    first_name = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Имя',
    )
    last_name = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Фамилия',
    )
    middle_name = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Отчество',
    )

    # Данные по адресу.
    address = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Полный адрес',
    )
    country = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Страна',
    )
    region = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Город',
    )
    city_area = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Область, округ',
    )
    city_district = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Район',
    )

    # Контактная информация.
    phone = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Телефон, относящийся к бизнесу',
    )
    email = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Email, относящийся к бизнесу',
    )
    site = fields.CharField(
        max_length=config.MAX_STRING_LENGTH,
        null=True,
        description='Сайт, относящийся к бизнесу',
    )
    created = fields.DatetimeField(
        auto_now_add=True,
        description='Дата создания бизнеса в БД',
    )

    def __str__(self):
        return f'{self.type}. ИНН - {self.inn}'
