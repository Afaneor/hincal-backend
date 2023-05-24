import django_filters

from server.apps.hincal.api.serializers import IndicatorSerializer
from server.apps.hincal.models import Indicator
from server.apps.services.filters_mixins import CreatedUpdatedDateFilterMixin
from server.apps.services.views import BaseModelViewSet


class IndicatorFilter(
    CreatedUpdatedDateFilterMixin,
    django_filters.FilterSet,
):
    """Фильтр показателей бизнеса."""

    class Meta(object):
        model = Indicator
        fields = (
            'id',
            'business',
            'year',
        )


class IndicatorViewSet(BaseModelViewSet):
    """Экономические показатели ИП, физического лица или компании."""

    serializer_class = IndicatorSerializer
    queryset = Indicator.objects.select_related('business')
    search_fields = (
        'business__short_business_name',
        'business__sector',
    )
    ordering_fields = '__all__'
    filterset_class = IndicatorFilter

    def get_queryset(self):
        """Выдача экономических показателей.

        Суперпользователь видит все показатели.
        Остальные видят показатели в рамках своего бизнеса.
        """
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_superuser:
            return queryset

        if user.is_anonymous:
            return queryset.none()

        return queryset.filter(
            business__in=user.businesses.all()
        )
