from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.apps.hincal.models import Report, Equipment
from server.apps.hincal.services.enums import (
    BusinessSector,
    BusinessSubSector,
    TerritorialLocation,
)
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

    sectors = serializers.ListField(
        child=serializers.CharField(),
        required=True,
    )
    sub_sectors = serializers.ListField(
        child=serializers.CharField(),
    )
    from_staff = serializers.IntegerField()
    to_staff = serializers.IntegerField()
    territorial_locations = serializers.ListField(
        child=serializers.CharField(),
    )
    from_land_area = serializers.IntegerField()
    to_land_area = serializers.IntegerField()
    from_property_area = serializers.IntegerField()
    to_property_area = serializers.IntegerField()
    equipment = serializers.PrimaryKeyRelatedField(
        queryset=Equipment.objects.all(),
        many=True,
    )
    is_accounting = serializers.BooleanField()
    is_patent = serializers.BooleanField()
    other = serializers.JSONField()

    def validate_sectors(self, sectors):
        """Валидация сектора."""
        for sector in sectors:
            if sector not in BusinessSector.value:
                raise ValidationError(
                    {'sectors': [_('Вы выбрали некорректный сектор')]},
                )
        return sectors

    def validate_sub_sectors(self, sub_sectors):
        """Валидация подсектора."""
        for sub_sector in sub_sectors:
            if sub_sector not in BusinessSubSector.value:
                raise ValidationError(
                    {'sub_sectors': [_('Вы выбрали некорректный подсектор')]},
                )
        return sub_sectors

    def validate_territorial_locations(self, territorial_locations):
        """Валидация районов расположения."""
        for territorial_location in territorial_locations:
            if territorial_location not in TerritorialLocation.value:
                raise ValidationError(
                    {
                        'territorial_locations': [
                            _(
                                'Вы выбрали некорректное территориальное ' +
                                'расположение',
                            ),
                        ],
                    },
                )
        return territorial_locations
