import django_filters

from server.apps.support.api.serializers import AreaSerializer
from server.apps.support.models import Area
from server.apps.services.filters_mixins import (
    CreatedUpdatedDateFilterMixin,
    TagFilterMixin,
)
from server.apps.services.views import BaseReadOnlyViewSet


class AreaFilter(
    TagFilterMixin,
    CreatedUpdatedDateFilterMixin,
    django_filters.FilterSet,
):
    """Фильтр мер поддержки."""

    title = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains')

    class Meta(object):
        model = Area
        fields = (
            'title',
            'tags',
            'address',
            'territorial_location',
        )


class AreaViewSet(BaseReadOnlyViewSet):
    """Площадки для производства. Просмотр."""

    serializer_class = AreaSerializer
    queryset = Area.objects.select_related(
        'territorial_location'
    ).prefetch_related('tags')
    ordering_fields = '__all__'
    search_fields = (
        'title',
        'address',
    )
    filterset_class = AreaFilter

    def get_queryset(self):  # noqa: WPS615
        """Выдача площадок для производства.

        Все видят только актуальные меры.
        """

        return super().get_queryset()
