import django_filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from server.apps.hincal.api.serializers import (
    CreateReportSerializer,
    ReportSerializer,
)
from server.apps.hincal.models import Report
from server.apps.hincal.services.create_report import ReportWithContext
from server.apps.services.filters_mixins import (
    CreatedUpdatedDateFilterMixin,
    UserFilterMixin,
)
from server.apps.services.views import RetrieveListCreateDeleteViewSet, \
    RetrieveListDeleteViewSet


class ReportFilter(
    UserFilterMixin,
    CreatedUpdatedDateFilterMixin,
    django_filters.FilterSet,
):
    """Фильтр отчетов."""

    class Meta(object):
        model = Report
        fields = (
            'id',
            'user',
            'user_email',
            'user_username',
            'user_first_name',
            'user_last_name',
            'user_middle_name',
        )


class ReportViewSet(RetrieveListDeleteViewSet):
    """Отчет."""

    serializer_class = ReportSerializer
    create_serializer_class = CreateReportSerializer
    queryset = Report.objects.select_related('user')
    search_fields = (
        'user_email',
        'user_username',
        'user_first_name',
        'user_last_name',
        'user_middle_name',
    )
    ordering_fields = '__all__'
    filterset_class = ReportFilter

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
            report__in=user.reports.all()
        )

    @action(
        ['POST'],
        url_path='calculator',
        detail=False,
        serializer_class=CreateReportSerializer,
    )
    def calculator(self, request):
        """Расчет расходов.

        Калькулятор для расчета расходов.

        Доступно: любому пользователю.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = ReportWithContext(
            user=request.user,
            data=serializer.validated_data,
        ).formation_report()

        return Response(
            data=ReportSerializer(report).data,
            status=status.HTTP_201_CREATED,
        )
