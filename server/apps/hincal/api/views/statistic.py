import django_filters
from django.db import models

from server.apps.hincal.api.serializers import StatisticSerializer
from server.apps.hincal.models import Statistic

from server.apps.services.filters_mixins import UserFilterMixin
from server.apps.services.views import BaseReadOnlyViewSet


class StatisticFilter(UserFilterMixin, django_filters.FilterSet):
    """Фильтр статистики."""

    class Meta(object):
        model = Statistic
        fields = (
            'id',
            'user',
            'user_email',
            'user_username',
            'user_first_name',
            'user_last_name',
            'user_middle_name',
        )


class StatisticViewSet(BaseReadOnlyViewSet):
    """Общая статистика по системе и для пользователя."""

    serializer_class = StatisticSerializer
    queryset = Statistic.objects.select_related('user')
    search_fields = (
        'user_email',
        'user_username',
        'user_first_name',
        'user_last_name',
        'user_middle_name',
    )
    ordering_fields = '__all__'
    filterset_class = StatisticFilter

    def get_queryset(self):
        """Выдача статистики.

        Суперпользователь видит всю статистику.
        Остальные видят свою статистику и общую (user=None).
        """
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_superuser:
            return queryset

        if user.is_authenticated:
            return queryset.filter(
                models.Q(user=user) |
                models.Q(user__isnull=True)
            )

        return queryset.filter(
            models.Q(user__isnull=True)
        )

