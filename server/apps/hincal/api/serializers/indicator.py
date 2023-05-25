from rest_framework import serializers

from server.apps.hincal.models import Indicator
from server.apps.services.serializers import ModelSerializerWithPermission


class IndicatorSerializer(ModelSerializerWithPermission):
    """Экономические показатели ИП, физического лица или компании."""

    class Meta(object):
        model = Indicator
        fields = (
            'id',
            'business',
            'year',
            'average_number_of_staff',
            'average_salary_of_staff',
            'taxes_to_the_budget',
            'income_tax',
            'property_tax',
            'land_tax',
            'personal_income_tax',
            'transport_tax',
            'other_taxes',
            'permission_rules',
            'created_at',
            'updated_at',
        )
