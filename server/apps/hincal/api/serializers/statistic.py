from rest_framework import serializers

from server.apps.hincal.models import Statistic
from server.apps.services.serializers import ModelSerializerWithPermission
from server.apps.user.api.serializers import BaseInfoUserSerializer


class StatisticSerializer(ModelSerializerWithPermission):
    """Общая статистика по системе и для пользователя."""

    user = BaseInfoUserSerializer()

    class Meta(object):
        model = Statistic
        fields = (
            'id',
            'user',
            'popular_sector',
            'average_investment_amount',
            'total_investment_amount',
            'amount_of_use_of_the_calculator',
            'permission_rules',
            'created_at',
            'updated_at',
        )
