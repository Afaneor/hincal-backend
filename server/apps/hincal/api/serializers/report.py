from rest_framework import serializers

from server.apps.hincal.models import Report
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

    sector = serializers.ListField(
        child=serializers.CharField(),
    )
    from_staff = serializers.IntegerField()
    to_staff = serializers.IntegerField()
    location_area = serializers.ListField(
        child=serializers.CharField(),
    )
    from_land_area = serializers.IntegerField()
    to_land_area = serializers.IntegerField()
    from_property_area = serializers.IntegerField()
    to_property_area = serializers.IntegerField()
    equipment = serializers.ListField(
        child=serializers.CharField(),
    )
    is_accounting = serializers.BooleanField()
    is_patent = serializers.BooleanField()
    other = serializers.JSONField()
