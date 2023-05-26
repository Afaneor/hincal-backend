from taggit.serializers import TagListSerializerField

from server.apps.blog.models import Support

from server.apps.services.serializers import ModelSerializerWithPermission


class SupportSerializer(ModelSerializerWithPermission):
    """Сериалайзер мер поддержки."""

    tags = TagListSerializerField()

    class Meta(object):
        model = Support
        fields = (
            'id',
            'preview_image',
            'title',
            'text',
            'tags',
            'site',
            'is_actual',
            'created_at',
            'updated_at',
            'permission_rules',
        )
