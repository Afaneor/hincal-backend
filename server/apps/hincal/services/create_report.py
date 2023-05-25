from typing import Optional, Union

from django.contrib.auth.models import AnonymousUser
from django.db import models

from server.apps.hincal.api.serializers import (
    BusinessForReportSerializer,
)
from server.apps.hincal.models import Archive, Indicator, Equipment, Business, \
    Report
from server.apps.hincal.services.enums import (
    BusinessSector,
    BusinessSubSector,
    TerritorialLocation,
)
from server.apps.hincal.services.report_context import (
    ReportContextDataClass,
)
from server.apps.user.models import User


class ReportWithContext(object):
    """Формирование context для отчета."""

    archive, created = Archive.objects.get_or_create(is_actual=True)

    def __init__(
        self,
        data: dict,
        user: Optional[Union[User, AnonymousUser]],
    ):
        """Инициализация переменных для работы."""
        self.user = user
        self.data = data
        # Верхний и нижний уровни погрешности. Уменьшаем или увеличиваем
        # переданные показатели.
        self.lower_margin_error = 0.9
        self.upper_margin_error = 1.1

    def get_filter_with_correct_sector(self) -> models.Q:
        """Получение фильтра с корректным сектором."""
        if sectors := self.data.get('sectors'):
            return models.Q(business__sector__in=sectors)

        else:
            return models.Q(business__sector__in=BusinessSector.values)

    def get_filter_with_correct_sub_sector(self) -> models.Q:
        """Получение фильтра с корректным подсектором."""
        # Если выбран подсектор, то ищем совпадения и по сектору и
        # по подсектору. Иначе ищем по всем доступным.
        if sub_sectors := self.data.get('sub_sectors'):
            return models.Q(business__sub_sector__in=sub_sectors)
        else:
            return models.Q(business__sub_sector__in=BusinessSubSector.values)

    def get_filter_with_correct_staff(self) -> models.Q:
        """Получение фильтра с корректным персоналом.

        Если персонала не передан, то ищем с любыми значениями.
        """
        from_staff = self.data.get('from_staff', None)
        to_staff = self.data.get('to_staff', from_staff)
        if from_staff and to_staff:
            return models.Q(
                models.Q(average_number_of_staff__gte=self.data.get('from_staff') * self.lower_margin_error) &  # noqa: E501
                models.Q(average_number_of_staff__lte=self.data.get('to_staff') * self.upper_margin_error)  # noqa: E501
            )
        return models.Q()

    def get_filter_with_correct_location(self) -> models.Q:
        """Получение фильтра с корректным территориальным расположением."""
        # Eсли локация не передана, ищем по всем доступным.
        if territorial_locations := self.data.get('territorial_locations'):
            return models.Q(
                models.Q(business__territorial_location__in=territorial_locations)  # noqa: E501
            )
        else:
            return models.Q(
                models.Q(business__territorial_location__in=TerritorialLocation.values)  # noqa: E501
            )

    def get_value_by_territorial_locations(
        self,
        property_name: str,
    ):
        """Получение корректных числовых значений по переданным округам."""
        # Получаем территориальное расположение. Если передан список,
        # то проходимся по списку, берем все значения и берем их среднее.
        # В противном случае отдаем просто среднее значение по всем.
        if territorial_locations := self.data.get('territorial_locations'):
            average_value = 0
            for territorial_location in territorial_locations:
                archive = getattr(self.archive, property_name)
                average_value += archive.get(territorial_location)

            return average_value // len(territorial_locations)

        return self.archive.land_tax_rate.get('OTHER')

    def get_value_by_need_patent(
        self,
        property_name: str,
    ):
        """Получение корректных числовых значений.

        Рассчитываем размер налога по патентной системе.
        """
        if sectors := self.data.get('sectors'):
            average_value = 0
            for sector in sectors:
                archive = getattr(self.archive, property_name)
                average_value += archive.get(sector)

            return average_value // len(sectors)

        return self.archive.land_tax_rate.get('OTHER')

    def get_filter_with_correct_land_area(self) -> models.Q:
        """Получение фильтра с корректной площадью земельного участка."""
        from_land_area = self.data.get('from_land_area', None)
        to_land_area = self.data.get('to_land_area', from_land_area)
        # Если не передан размер земли, то ищем по всем доступным. Поскольку
        # данных по земли нет, то переводим размер земли в размер налога
        # на землю.
        if from_land_area and to_land_area:
            #  Средний размер площади земельного участка.
            average_land_area = (from_land_area + to_land_area) // 2
            # Размер налога.
            land_tax = (
                average_land_area *
                self.get_value_by_territorial_locations(
                    property_name='land_cadastral_value',
                ) *
                self.archive.land_tax_rate
            )

            return models.Q(
                models.Q(land_tax__gte=land_tax * self.archive.lower_tax_margin_error) &
                models.Q(land_tax__lte=land_tax * self.archive.upper_tax_margin_error)
            )

        return models.Q()

    def get_filter_with_correct_property_area(self) -> models.Q:
        """Получение фильтра с корректной площадью объектов капитального строительства."""
        from_property_area = self.data.get('from_property_area', None)
        to_property_area = self.data.get('to_property_area', from_property_area)
        # Если не передан размер имущества, то ищем по всем доступным. Поскольку
        # данных по имуществу нет, то переводим размер имущества в размер налога
        # на имущество.
        if from_property_area and to_property_area:
            #  Средний размер площади имущества.
            average_property_area = (from_property_area + to_property_area) // 2
            # Размер налога.
            property_tax = (
                average_property_area *
                self.get_value_by_territorial_locations(
                    property_name='property_cadastral_value',
                ) *
                self.archive.property_tax_rate
            )

            return models.Q(
                models.Q(property_tax__gte=property_tax * self.archive.lower_tax_margin_error) &
                models.Q(property_tax__lte=property_tax * self.archive.upper_tax_margin_error)
            )

        return models.Q()

    def get_indicators(self) -> models.QuerySet[Indicator]:
        """Получение корректных показателей для формирования отчета."""
        correct_sector = self.get_filter_with_correct_sector()
        correct_sub_sector = self.get_filter_with_correct_sub_sector()
        correct_staff = self.get_filter_with_correct_staff()
        correct_land_area = self.get_filter_with_correct_land_area()
        correct_property_area = self.get_filter_with_correct_property_area()
        correct_location = self.get_filter_with_correct_location()
        if (
            indicators := Indicator.objects.filter(
                models.Q(
                    correct_sector &
                    correct_sub_sector &
                    correct_staff &
                    correct_land_area &
                    correct_property_area &
                    correct_location
                )
            )
        ):
            return indicators

        if (
            indicators := Indicator.objects.filter(
                models.Q(
                    correct_sector &
                    correct_sub_sector &
                    correct_staff &
                    correct_land_area &
                    correct_property_area
                )
            )
        ):
            return indicators

        if (
            indicators := Indicator.objects.filter(
                models.Q(
                    correct_sector &
                    correct_sub_sector &
                    correct_staff &
                    correct_land_area
                )
            )
        ):
            return indicators

        if (
            indicators := Indicator.objects.filter(
                models.Q(
                    correct_sector &
                    correct_sub_sector &
                    correct_staff
                )
            )
        ):
            return indicators

        if (
            indicators := Indicator.objects.filter(
                models.Q(
                    correct_sector &
                    correct_sub_sector
                )
            )
        ):
            return indicators

        if indicators := Indicator.objects.filter(correct_sector):
            return indicators

        return Indicator.objects.all()

    def get_patent_costs(self):
        """Получить размер возможных налогов на патент."""
        if self.data.get('need_patent'):
            return self.get_value_by_need_patent(
                property_name='possible_income_from_patent',
            ) * self.archive.patent_tax_rate
        return 0

    def get_registration_costs(self):
        """Получить расходны на регистрации."""
        if self.data.get('need_registration'):
            return self.archive.registration_costs.get(
                self.data.get('type_business', 'other'),
                0,
            )
        return 0

    def get_accounting_costs(self):
        """Получить расходны на ведение бухгалтерского учета."""
        if self.data.get('need_accounting'):
            accounting_costs = self.archive.cost_accounting.get(
                self.data.get('type_business', 'other'),
                {}
            )
            return accounting_costs.get(
                self.data.get('type_tx_system', 'other'),
            )
        return 0

    def get_equipment_costs(self):
        """Получение стоимости оборудования."""
        if equipment := Equipment.objects.filter(
            id__in=self.data.get('equipment'),
        ).aggregate(
            equipment_costs=models.Sum('cost')
        ).get('equipment_costs'):
            return equipment
        return 0

    def formation_report(self):
        """Формирование контекста."""
        indicators = self.get_indicators()
        avg_indicators = indicators.aggregate(
            avg_number_of_staff=models.Avg('average_number_of_staff'),
            avg_salary_of_staff=models.Avg('average_salary_of_staff'),
            avg_taxes_to_the_budget=models.Avg('taxes_to_the_budget'),
            avg_income_tax=models.Avg('income_tax'),
            avg_property_tax=models.Avg('property_tax'),
            avg_land_tax=models.Avg('land_tax'),
            avg_personal_income_tax=models.Avg('personal_income_tax'),
            avg_transport_tax=models.Avg('transport_tax'),
            avg_other_taxes=models.Avg('other_taxes'),
        )

        business = Business.objects.filter(user=self.user).first()
        context = ReportContextDataClass(
            business=BusinessForReportSerializer(business).data if business else {},
            initial_data=self.data,

            avg_number_of_staff=avg_indicators.get('avg_number_of_staff'),
            avg_salary_of_staff=avg_indicators.get('avg_salary_of_staff'),
            avg_taxes_to_the_budget=avg_indicators.get('avg_taxes_to_the_budget'),
            avg_income_tax=avg_indicators.get('avg_income_tax'),

            avg_property_tax=avg_indicators.get('avg_property_tax'),
            avg_land_tax=avg_indicators.get('avg_land_tax'),
            avg_personal_income_tax=avg_indicators.get('avg_personal_income_tax'),
            avg_transport_tax=avg_indicators.get('avg_transport_tax'),
            avg_other_taxes=avg_indicators.get('avg_other_taxes'),

            equipment_costs=self.get_equipment_costs(),
            accounting_costs=self.get_accounting_costs(),
            registration_costs=self.get_registration_costs(),
        )
        return Report.objects.create(
            user=self.user,
            initial_data=self.data,
            context=context.__dict__,
        )
