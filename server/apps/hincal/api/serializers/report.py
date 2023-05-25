from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.apps.hincal.models import Report, Equipment
from server.apps.hincal.services.enums import (
    BusinessSector,
    BusinessSubSector,
    TerritorialLocation, TypeBusiness, TypeTaxSystem,
)
from server.apps.hincal.services.validate_report import check_range
from server.apps.services.serializers import ModelSerializerWithPermission


class ReportSerializer(ModelSerializerWithPermission):
    """Отчет."""

    class Meta(object):
        model = Report
        fields = (
            'id',
            'user',
            'initial_data',
            'context',
            'permission_rules',
            'created_at',
            'updated_at',
        )


class CreateReportSerializer(serializers.Serializer):
    """Создание отчета."""

    type_business = serializers.ChoiceField(
        choices=[TypeBusiness.LEGAL, TypeBusiness.INDIVIDUAL],
        required=True,
    )
    sectors = serializers.MultipleChoiceField(
        choices=BusinessSector.choices,
        required=True,
    )
    sub_sectors = serializers.MultipleChoiceField(
        choices=BusinessSubSector.choices,
    )
    from_staff = serializers.IntegerField()
    to_staff = serializers.IntegerField()
    territorial_locations = serializers.MultipleChoiceField(
        choices=TerritorialLocation.choices,
    )
    from_land_area = serializers.IntegerField()
    to_land_area = serializers.IntegerField()
    from_property_area = serializers.IntegerField()
    to_property_area = serializers.IntegerField()
    equipment = serializers.PrimaryKeyRelatedField(
        queryset=Equipment.objects.all(),
        many=True,
    )
    type_tax_system = serializers.ChoiceField(
        choices=TypeTaxSystem.choices,
        default=TypeTaxSystem.OSN,
    )
    need_accounting = serializers.BooleanField()
    need_registration = serializers.BooleanField()

    other = serializers.JSONField()

    def validate_type_business(self, type_business):
        """Валидация типа."""
        if type_business not in {TypeBusiness.LEGAL, TypeBusiness.INDIVIDUAL}:
            raise ValidationError(
                {'type_business': [
                    _(
                        'Ведение бизнеса может только ИП или юридическое лицо',
                    ),
                ]},
            )
        return type_business

    def validate_sectors(self, sectors):
        """Валидация сектора."""
        for sector in sectors:
            if sector not in BusinessSector.values:
                raise ValidationError(
                    {'sectors': [_('Вы выбрали некорректный сектор')]},
                )
        # Распаковка нужна для будущей сериализации в json.
        return [*sectors]

    def validate_sub_sectors(self, sub_sectors):
        """Валидация подсектора."""
        for sub_sector in sub_sectors:
            if sub_sector not in BusinessSubSector.values:
                raise ValidationError(
                    {'sub_sectors': [_('Вы выбрали некорректный подсектор')]},
                )
        # Распаковка нужна для будущей сериализации в json.
        return [*sub_sectors]

    def validate_territorial_locations(self, territorial_locations):
        """Валидация районов расположения."""
        for territorial_location in territorial_locations:
            if territorial_location not in TerritorialLocation.values:
                raise ValidationError(
                    {'territorial_locations': [
                        _(
                            'Вы выбрали некорректное территориальное ' +
                            'расположение',
                        ),
                    ]},
                )
        # Распаковка нужна для будущей сериализации в json.
        return [*territorial_locations]

    def validate_type_tax_system(self, type_tax_system):
        """Валидация типа системы налогооблажения."""
        if type_tax_system not in TypeTaxSystem.values:
            raise ValidationError(
                {'type_tax_system': [_('Некорректная система налогооблажения')]},
            )
        return type_tax_system

    def validate(self, attrs):
        """Общая валидация.

        У юридического лица нет патентной системы налогооблажения.
        """
        type_business = attrs.get('type_business')
        type_tax_system = attrs.get('type_tax_system')
        if type_business == TypeBusiness.LEGAL and type_tax_system == TypeTaxSystem.PATENT:
            raise ValidationError(
                {'type_tax_system':
                     [_('У юридического лица нет патентной системы налогооблажения')]
                 },
            )
        # Проверка диапазона по сотрудникам.
        attrs = check_range(
            attrs=attrs,
            from_name_value='from_staff',
            to_name_value='to_staff',
        )
        # Проверка диапазона по земле.
        attrs = check_range(
            attrs=attrs,
            from_name_value='from_land_area',
            to_name_value='to_land_area',
        )
        # Проверка диапазона по имуществу.
        attrs = check_range(
            attrs=attrs,
            from_name_value='from_property_area',
            to_name_value='to_property_area',
        )

        return attrs
