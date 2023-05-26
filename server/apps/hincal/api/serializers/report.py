from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.apps.hincal.models import (
    Report,
    Equipment,
    Sector,
    SubSector,
    TerritorialLocation,
)
from server.apps.hincal.services.enums import (
    TypeBusiness,
    TypeBusinessForCalculator,
    TypeTaxSystem,
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
        choices=TypeBusinessForCalculator.choices,
        required=True,
    )
    sectors = serializers.PrimaryKeyRelatedField(
        queryset=Sector.objects.all(),
        many=True,
        required=True,
    )
    sub_sectors = serializers.PrimaryKeyRelatedField(
        queryset=SubSector.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )
    from_staff = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    to_staff = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    territorial_locations = serializers.PrimaryKeyRelatedField(
        queryset=TerritorialLocation.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )
    from_land_area = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    to_land_area = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    from_property_area = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    to_property_area = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    equipments = serializers.PrimaryKeyRelatedField(
        queryset=Equipment.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )
    type_tax_system = serializers.ChoiceField(
        choices=TypeTaxSystem.choices,
        default=TypeTaxSystem.OSN,
    )
    need_accounting = serializers.BooleanField(default=False)
    need_registration = serializers.BooleanField(default=False)

    other = serializers.JSONField(
        allow_null=True,
    )

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
                {'type_tax_system': [_('У юридического лица нет патентной системы налогооблажения')]},
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
