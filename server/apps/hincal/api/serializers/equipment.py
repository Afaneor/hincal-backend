from server.apps.hincal.models import Equipment
from server.apps.services.serializers import ModelSerializerWithPermission
from server.apps.user.api.serializers import BaseInfoUserSerializer


class EquipmentSerializer(ModelSerializerWithPermission):
    """Сериалайзер оборудования."""

    class Meta(object):
        model = Equipment
        fields = (
            'id',
            'name',
            'cost',
            'permission_rules',
            'created_at',
            'updated_at',
        )
