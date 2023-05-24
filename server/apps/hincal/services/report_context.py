from typing import Optional

from django.contrib.auth.models import AnonymousUser
from django.db import models

from server.apps.hincal.models import Indicator
from server.apps.hincal.services.enums import BusinessSector, BusinessSubSector, \
    TerritorialLocation
from server.apps.user.models import User


class ReportContext(object):
    """Формирование context для отчета."""

    def __int__(
        self,
        user: Optional[User, AnonymousUser],
        data: dict,
        margin_error: bool,
    ):
        """Инициализация переменных для работы."""
        self.user = user
        self.data = data
        # Верхний и нижний уровни погрешности. Уменьшаем или увеличиваем
        # переданные показатели.
        if margin_error:
            self.lower_margin_error = 0.9
            self.upper_margin_error = 1.1
        else:
            self.lower_margin_error = 1
            self.upper_margin_error = 1

    def get_filter_with_correct_sector(self) -> models.Q:
        """Получение фильтра с корректным сектором."""
        filters = models.Q()
        if sectors := self.data.get('sectors'):
            filters = models.Q(
                filters |
                models.Q(business__sector__in=sectors)
            )
            # Если выбран подсектор, то ищем совпадения и по сектору и
            # по подсектору.
            if sub_sectors := self.data.get('sub_sectors'):
                filters = models.Q(
                    filters &
                    models.Q(business__sub_sector__in=sub_sectors)
                )
            else:
                filters = models.Q(
                    filters &
                    models.Q(business__sub_sector__in=BusinessSubSector.value)
                )
        else:
            filters = models.Q(
                filters &
                models.Q(business__sector__in=BusinessSector.value)
            )


        return filters

    def get_filter_with_correct_staff(self):
        """Получение фильтра с корректным персоналом."""
        return models.Q(
            models.Q(average_number_of_employees__gte=self.data.get('from_staff') * self.lower_margin_error) &  # noqa: E501
            models.Q(average_number_of_employees__lte=self.data.get('to_staff')* self.upper_margin_error)  # noqa: E501
        )

    def get_filter_with_correct_location(self):
        """Получение фильтра с корректным территориальным расположением."""
        filters = models.Q()
        if territorial_locations := self.data.get('territorial_locations'):
            filters = models.Q(
                filters |
                models.Q(business__territorial_location__in=territorial_locations)  # noqa: E501
            )
        else:
            filters = models.Q(
                filters |
                models.Q(business__territorial_location__in=TerritorialLocation.values)  # noqa: E501
            )
        return filters

    def get_filter_with_correct_land_area(self):
        """"""


    def get_indicators(self) -> models.QuerySet[Indicator]:
        """Получение корректных показателей для формирования отчета."""
        filters = models.Q(
            self.get_filter_with_correct_sector() &
            self.get_filter_with_correct_staff() &
            self.get_filter_with_correct_location() &
        )
        return

    def formation_context(self):
        """Формирование контекста."""
        indicators = self.get_indicators()
