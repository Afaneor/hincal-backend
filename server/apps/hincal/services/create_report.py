from typing import Optional, Union, Set, Tuple, List

from django.contrib.auth.models import AnonymousUser
from django.db import models

from server.apps.hincal.api.serializers import (
    BusinessForReportSerializer,
)
from server.apps.hincal.models import Archive, BusinessIndicator, Equipment, \
    Business, \
    Report, Sector
from server.apps.hincal.services.enums import (
    BusinessSector,
    BusinessSubSector,
    TerritorialLocation, TypeBusiness,
)
from server.apps.hincal.services.report_context import (
    ReportContextDataClass,
)
from server.apps.user.models import User


class ReportWithContext(object):
    """Формирование context для отчета."""

    _archive: Archive = None

    # Верхний и нижний уровни погрешности. Уменьшаем или увеличиваем
    # переданные показатели.
    LOWER_MARGIN_ERROR = 0.8
    UPPER_MARGIN_ERROR = 1.2

    # Переменные, которые будут получены в ходе расчетов:
    # Среднее количество работников.
    avg_number_of_staff = 0
    # Средний размер заработной платы по отраслям.
    avg_salary_of_staff = 0
    # Общий фонд заработной платы всех сотрудников.
    all_salary = 0
    # Средний размер площади земельного участка.
    avg_land_area = 0
    # Средняя кадастровая стоимость на землю.
    avg_land_cadastral_value = 0
    # Размер налога на землю.
    avg_land_tax = 0
    # Средний размер площади имущества.
    avg_property_area = 0
    # Средняя кадастровая стоимость на имущество.
    avg_property_cadastral_value = 0
    # Размер налога на имущество.
    avg_property_tax = 0
    # Средний возможный доход по патентной системе.
    possible_income_from_patent = 0
    # Средний размер налога на патент.
    avg_patent_tax = 0
    # Расходны на регистрацию.
    avg_registration_costs = 0
    # Расходны на ведение бухгалтерского учета.
    avg_accounting_costs = 0
    # Расходны на оборудование.
    equipments = 0

    report: Report = None

    def __init__(
        self,
        data: dict,
        user: Optional[Union[User, AnonymousUser]],
    ):
        """Инициализация переменных для работы."""
        self.user = user if user.is_authenticated else None
        self.data = data

        self.sectors = data.get('sectors')

    @property
    def archive(self):
        """Получение Архива."""
        if not ReportWithContext._archive:  # noqa: WPS437
            ReportWithContext._archive, created = Archive.objects.get_or_create(
                is_actual=True,
            )
        return ReportWithContext._archive  # noqa: WPS437

    # FIXME: Проверить логику.
    def create_tags(self) -> None:
        """Прикрепление тегов к отчету."""
        for sector in self.sectors:
            self.report.tags.add(sector.slug, sector.tags)
        self.report.save()

    def get_filter_with_correct_sector(self) -> models.Q:
        """Получение фильтра с корректным сектором."""
        if self.sectors:
            return models.Q(business__sector__in=self.sectors)
        else:
            return models.Q()

    def get_filter_with_correct_sub_sector(self) -> models.Q:
        """Получение фильтра с корректным подсектором."""
        # Если выбран подсектор, то ищем совпадения и по сектору и
        # по подсектору. Иначе ищем по всем доступным.
        if sub_sectors := self.data.get('sub_sectors'):
            return models.Q(business__sub_sector__in=sub_sectors)
        else:
            return models.Q()

    def get_filter_with_correct_staff(self) -> models.Q:
        """Получение фильтра с корректным персоналом.

        Если персонала не передан, то ищем с любыми значениями.
        """
        from_staff = self.data.get('from_staff', None)
        to_staff = self.data.get('to_staff', from_staff)

        if from_staff and to_staff:
            self.avg_number_of_staff = (from_staff + to_staff) / 2
            return models.Q(
                models.Q(average_number_of_staff__gte=self.data.get('from_staff') * self.LOWER_MARGIN_ERROR) &
                models.Q(average_number_of_staff__lte=self.data.get('to_staff') * self.UPPER_MARGIN_ERROR)
            )
        return models.Q()

    def get_filter_with_correct_location(self) -> models.Q:
        """Получение фильтра с корректным территориальным расположением."""
        # Если локация не передана, ищем по всем доступным.
        if territorial_locations := self.data.get('territorial_locations'):
            return models.Q(
                business__territorial_location__in=territorial_locations
            )
        else:
            return models.Q()

    def get_value_by_territorial_locations(
        self,
        property_name: str,
    ) -> Union[int, float]:
        """Получение корректных числовых значений по переданным округам."""
        # Получаем территориальное расположение. Если передан список,
        # то проходимся по списку, берем все значения и берем их среднее.
        # В противном случае отдаем просто среднее значение по всем.
        archive = getattr(self.archive, property_name, None)
        if archive:
            if territorial_locations := self.data.get('territorial_locations'):
                average_value = 0
                # Из атрибута объекта берем нужную информацию по округу.
                for territorial_location in territorial_locations:
                    average_value += archive.get(territorial_location)

                return average_value / len(territorial_locations)

            return archive.get('other')

        return 0

    def get_filter_with_correct_land_area(self) -> models.Q:
        """Получение фильтра с корректной площадью земельного участка."""
        from_land_area = self.data.get('from_land_area', None)
        to_land_area = self.data.get('to_land_area', from_land_area)
        # Если не передан размер земли, то ищем по всем доступным. Поскольку
        # данных по земли нет, то переводим размер земли в размер налога
        # на землю.
        if from_land_area and to_land_area:
            #  Средний размер площади земельного участка.
            self.avg_land_area = (from_land_area + to_land_area) / 2
            # Средняя кадастровая стоимость на землю.
            self.avg_land_cadastral_value = self.get_value_by_territorial_locations(
                property_name='land_cadastral_value',
            )
            # Размер налога.
            self.avg_land_tax = (
                self.avg_land_area *
                self.avg_land_cadastral_value *
                self.archive.land_tax_rate
            )

            return models.Q(
                models.Q(land_tax__gte=self.avg_land_tax * self.archive.lower_tax_margin_error) &
                models.Q(land_tax__lte=self.avg_land_tax * self.archive.upper_tax_margin_error)
            )

        return models.Q()

    def get_filter_with_correct_property_area(self) -> models.Q:
        """Получение фильтра с корректной площадью объектов."""
        from_property_area = self.data.get('from_property_area', None)
        to_property_area = self.data.get('to_property_area', from_property_area)
        # Если не передан размер имущества, то ищем по всем доступным. Поскольку
        # данных по имуществу нет, то переводим размер имущества в размер налога
        # на имущество.
        if from_property_area and to_property_area:
            # Средний размер площади имущества.
            self.avg_property_area = (from_property_area + to_property_area) / 2
            # Средняя кадастровая стоимость на имущество.
            self.avg_property_cadastral_value = self.get_value_by_territorial_locations(
                    property_name='property_cadastral_value',
                )
            # Размер налога на имущество.
            self.avg_property_tax = (
                self.avg_property_area *
                self.avg_property_cadastral_value *
                self.archive.property_tax_rate
            )

            return models.Q(
                models.Q(property_tax__gte=self.avg_property_tax * self.archive.lower_tax_margin_error) &
                models.Q(property_tax__lte=self.avg_property_tax * self.archive.upper_tax_margin_error)
            )

        return models.Q()

    def get_value_by_sector(
        self,
        property_name: str,
    ):
        """Получение корректных числовых значений.

        Получаем корректные числовые значения по отрасли деятельности.
        """
        archive = getattr(self.archive, property_name, None)

        if archive:
            if self.sectors:
                average_value = 0
                for sector in self.sectors:
                    average_value += archive.get(sector)

                return average_value / len(self.sectors)

            return archive.get('other')

        return 0

    def get_business_indicators(self):
        """Получение корректных показателей для формирования отчета.

        Здесь мы ищем в бд реальный существующий бизнес, который подходит под
        наши критерии.
        Отдаем найденное пользователю.
        """
        correct_sector = self.get_filter_with_correct_sector()
        correct_sub_sector = self.get_filter_with_correct_sub_sector()
        correct_staff = self.get_filter_with_correct_staff()
        correct_land_area = self.get_filter_with_correct_land_area()
        correct_property_area = self.get_filter_with_correct_property_area()
        correct_location = self.get_filter_with_correct_location()
        if (
            business_indicators := BusinessIndicator.objects.filter(
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
            return (
                business_indicators,
                [
                    'sector',
                    'sub_sector',
                    'staff',
                    'land_area',
                    'property_area',
                    'location',
                ]
            )

        if (
            business_indicators := BusinessIndicator.objects.filter(
                models.Q(
                    correct_sector &
                    correct_sub_sector &
                    correct_staff &
                    correct_land_area &
                    correct_property_area
                )
            )
        ):
            return (
                business_indicators,
                ['sector', 'sub_sector', 'staff', 'land_area', 'property_area'],
            )

        if (
            business_indicators := BusinessIndicator.objects.filter(
                models.Q(
                    correct_sector &
                    correct_sub_sector &
                    correct_staff &
                    correct_land_area
                )
            )
        ):
            return (
                business_indicators,
                ['sector', 'sub_sector', 'staff', 'land_area'],
            )

        if (
            business_indicators := BusinessIndicator.objects.filter(
                models.Q(
                    correct_sector &
                    correct_sub_sector &
                    correct_staff
                )
            )
        ):
            return (
                business_indicators,
                ['sector', 'sub_sector', 'staff'],
            )

        if (
            business_indicators := BusinessIndicator.objects.filter(
                models.Q(
                    correct_sector &
                    correct_sub_sector
                )
            )
        ):
            return (
                business_indicators,
                ['sector', 'sub_sector'],
            )

        if business_indicators := BusinessIndicator.objects.filter(correct_sector):
            return (
                business_indicators,
                ['sector'],
            )

        return (
            BusinessIndicator.objects.all(),
            [],
        )

    def get_patent_costs(self) -> Union[float, int]:
        """Получить размер возможных налогов на патент.

        Доступно только для ИП.
        """
        avg_possible_income = 0
        if (
            self.data.get('need_patent') and
            self.data.get('type_business') == TypeBusiness.INDIVIDUAL
        ):
            for sector in self.sectors:
                avg_possible_income += sector.possible_income_from_patent

            self.possible_income_from_patent = (
                avg_possible_income /
                len(self.sectors)
            )
            self.avg_patent_tax = (
                self.possible_income_from_patent *
                self.archive.patent_tax_rate
            )

            return self.avg_patent_tax

        return 0

    def get_registration_costs(self) -> Union[float, int]:
        """Получить расходны на регистрации."""
        if self.data.get('need_registration'):
            self.avg_registration_costs = self.archive.registration_costs.get(
                self.data.get('type_business', 'other'),
                0,
            )

            return self.avg_registration_costs

        return 0

    def get_accounting_costs(self):
        """Получить расходны на ведение бухгалтерского учета."""
        if self.data.get('need_accounting'):
            accounting_costs = self.archive.cost_accounting.get(
                self.data.get('type_business', 'other'),
                {}
            )
            # Получаем словарь с верхней и нижней границей.
            accounting_costs_range = accounting_costs.get(
                self.data.get('type_tax_system', 'other'),
            )
            # Получаем средний размер расходов на ведение бухгалтерского учета.
            self.avg_accounting_costs = (
                (
                    accounting_costs_range.get('lower') +
                    accounting_costs_range.get('upper')
                ) / 2
            )

            return self.avg_accounting_costs

        return 0

    def get_equipment_costs(self):
        """Получение стоимости оборудования."""
        if equipments := Equipment.objects.filter(
            id__in=self.data.get('equipment'),
        ).aggregate(
            equipment_costs=models.Sum('cost')
        ).get('equipment_costs'):
            self.equipments = equipments

            return self.equipments

        return 0

    def formation_report(self):
        """Формирование контекста."""
        business_indicators, filters_key = self.get_business_indicators()
        avg_business_indicator = business_indicators.aggregate(
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

        business = Business.objects.filter(
            user=self.user,
            user__isnull=False
        ).first()
        context = ReportContextDataClass(
            # Информация по бизнесу.
            business=BusinessForReportSerializer(business).data if business else {},
            # Исходные данные.
            initial_data=self.data,

            # Показатели других бизнесов, которые есть в БД.
            avg_number_of_staff_by_business_indicators=avg_business_indicator.get('avg_number_of_staff'),
            avg_salary_of_staff_by_business_indicators=avg_business_indicator.get('avg_salary_of_staff'),
            avg_taxes_to_the_budget_by_business_indicators=avg_business_indicator.get('avg_taxes_to_the_budget'),
            avg_income_tax_by_business_indicators=avg_business_indicator.get('avg_income_tax'),
            avg_property_tax_by_business_indicators=avg_business_indicator.get('avg_property_tax'),
            avg_land_tax_by_business_indicators=avg_business_indicator.get('avg_land_tax'),
            avg_personal_income_tax_by_business_indicators=avg_business_indicator.get('avg_personal_income_tax'),
            avg_transport_tax_by_business_indicators=avg_business_indicator.get('avg_transport_tax'),
            avg_other_taxes_by_business_indicators=avg_business_indicator.get('avg_other_taxes'),

            # Рассчитанные показатели на основе простой математике.
            avg_number_of_staff_math=self.avg_number_of_staff,
            avg_salary_of_staff_math=self.get_avg_salary_of_staff(),
            all_salary=self.get_all_salary(),
            avg_personal_income_tax_math=self.get_avg_personal_income_tax(),

            avg_land_area_math=self.avg_land_area,
            avg_land_cadastral_value_math=self.avg_land_cadastral_value,
            avg_land_tax_math=self.avg_land_tax,

            avg_property_area_math=self.avg_property_area,
            avg_property_cadastral_value_math=self.avg_property_cadastral_value,
            avg_property_tax_math=self.avg_property_tax,

            avg_patent_tax_math=self.avg_patent_tax,

            equipment_costs=self.get_equipment_costs(),
            accounting_costs=self.get_accounting_costs(),
            registration_costs=self.get_registration_costs(),

            archive=self.archive,
        )
        correct_context = context.__dict__
        correct_context.pop('archive')

        initial_data = {}
        for key_data, value_data in self.data.items():
            if key_data == 'sectors':
                initial_data.update(
                    {'sectors': [sector.name for sector in value_data]}
                )
            elif key_data == 'sub_sectors':
                initial_data.update(
                    {'sub_sectors': [sub_sector.name for sub_sector in value_data]}
                )
            elif key_data == 'equipments':
                initial_data.update(
                    {'equipments': [equipment.name for equipment in value_data]}
                )
            else:
                initial_data.update({key_data: value_data})
        # FIXME: Убрать когда перепишу все.
        initial_data.pop('territorial_locations')
        correct_context.update({'initial_data': initial_data})
        self.report = Report.objects.create(
            user=self.user,
            initial_data=initial_data,
            context=correct_context,
        )
        self.create_tags()
        return self.report

    def get_avg_salary_of_staff(self):
        """Получение среднего размера зп исходя из отрасли."""
        avg_salary_of_staff = 0
        for sector in self.sectors:
            avg_salary_of_staff += sector.avg_salary_of_staff

        self.avg_salary_of_staff = avg_salary_of_staff / len(self.sectors)

        return self.avg_salary_of_staff

    def get_all_salary(self):
        """Общий размер заработной платы."""
        self.all_salary = self.avg_number_of_staff * self.avg_salary_of_staff
        return self.all_salary

    def get_avg_personal_income_tax(self):
        """Размер НДФЛ."""
        return self.all_salary * self.archive.personal_income_rate
