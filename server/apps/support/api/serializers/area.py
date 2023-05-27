from taggit.serializers import TagListSerializerField

from server.apps.hincal.api.serializers.territorial_location import (
    BaseTerritorialLocationSerializer,
)
from server.apps.support.models import Area

from server.apps.services.serializers import ModelSerializerWithPermission


class AreaSerializer(ModelSerializerWithPermission):
    """Сериалайзер площадок."""

    tags = TagListSerializerField()
    territorial_location = BaseTerritorialLocationSerializer()

    class Meta(object):
        model = Area
        fields = (
            'id',
            'preview_image',
            'title',
            'text',
            'territorial_location',
            'address',
            'site',
            'tags',
            'created_at',
            'updated_at',
            'permission_rules',
        )


class BaseAreaSerializer(ModelSerializerWithPermission):
    """Сериалайзер площадок для других сериалайзеров."""

    class Meta(object):
        model = Area
        fields = (
            'id',
            'preview_image',
            'title',
            'text',
            'address',
            'site',
        )
