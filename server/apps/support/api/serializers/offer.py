from taggit.serializers import TagListSerializerField

from server.apps.support.models import Offer

from server.apps.services.serializers import ModelSerializerWithPermission


class OfferSerializer(ModelSerializerWithPermission):
    """Сериалайзер партнерских предложений."""

    tags = TagListSerializerField()

    class Meta(object):
        model = Offer
        fields = (
            'id',
            'title',
            'text',
            'site',
            'extra_data',
            'tags',
            'created_at',
            'updated_at',
            'permission_rules',
        )
