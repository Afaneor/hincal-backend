from typing import Optional, Union

from django.contrib.auth.models import AnonymousUser
from django.db import models

from server.apps.hincal.api.serializers import (
    ArchiveForReportSerializer,
    BaseBusinessSerializer,
)
from server.apps.hincal.models import (
    Archive,
    BusinessIndicator,
    Equipment,
    Business,
    Report,
)
from server.apps.hincal.tasks import create_chat_gpt
from server.apps.hincal.services.enums import TypeBusiness
from server.apps.hincal.services.report_context import ReportContextDataClass
from server.apps.user.models import User


class ReportWithContext(object):
    """Формирование context для отчета."""

    _archive: Archive = None

    # Верхний и нижний уровни погрешности. Уменьшаем или увеличиваем
    # переданные показатели.
    LOWER_MARGIN_ERROR = 0.85
    UPPER_MARGIN_ERROR = 1.15

    # Переменные, которые будут получены в ходе расчетов:
    # Среднее количество работников.
    avg_number_of_staff: float = 0.0
    # Средний размер заработной платы по отраслям.
    avg_salary_of_staff: float = 0.0
    # Общий фонд заработной платы всех сотрудников.
    all_salary: float = 0.0
    # Средний размер площади земельного участка.
    avg_land_area: float = 0.0
    # Средняя кадастровая стоимость на землю.
    avg_land_cadastral_value: float = 0.0
    # Размер налога на землю.
    avg_land_tax: float = 0.0
    # Средний размер площади имущества.
    property_area: float = 0.0
    # Средняя кадастровая стоимость на имущество.
    avg_property_cadastral_value: float = 0.0
    # Размер налога на имущество.
    avg_property_tax_math: float = 0.0
    # Расходны на капитальное строительство.
    avg_capital_construction_costs_math: float = 0.0
    # Средний возможный доход по патентной системе.
    possible_income_from_patent: float = 0.0
    # Средний возможный доход.
    avg_possible_income: float = 0.0
    # Средний размер налога на патент.
    avg_patent_tax: float = 0.0
    # Расходны на регистрацию.
    avg_registration_costs: float = 0.0
    # Расходны на ведение бухгалтерского учета.
    avg_accounting_costs: float = 0.0
    # Расходны на оборудование.
    equipments: float = 0.0
    # Другие расходы представленные в виде строки.
    other_costs_str = ''
    # Список типов имущества.
    type_capital_construction = ''

    report: Report = None

    def __init__(
        self,
        data: dict,
        user: Optional[Union[User, AnonymousUser]],
    ):
        """Инициализация переменных для работы."""
        self.user = user if user.is_authenticated else None
        self.data = data

        self.sector = data.get('sector')
        self.territorial_locations = self.data.get('territorial_locations')

    @property
    def archive(self):
        """Получение Архива."""
        if not ReportWithContext._archive:  # noqa: WPS437
            ReportWithContext._archive, created = Archive.objects.get_or_create(
                is_actual=True,
            )
        return ReportWithContext._archive  # noqa: WPS437

    def create_tags(self) -> None:
        """Прикрепление тегов к отчету."""
        self.report.tags.add(
            self.sector.name,
            *self.sector.tags.values_list('name', flat=True),
        )

        self.report.save()

    def get_filter_with_correct_sector(self) -> models.Q:
        """Получение фильтра с корректным сектором."""
        if self.sector:
            return models.Q(business__sector=self.sector)
        else:
            return models.Q()

    def get_filter_with_correct_sub_sector(self) -> models.Q:
        """Получение фильтра с корректным подсектором."""
        # Если выбран подсектор, то ищем совпадения и по сектору и
        # по подсектору. Иначе ищем по всем доступным.
        if sub_sector := self.data.get('sub_sector'):
            return models.Q(business__sub_sector__in=sub_sector)
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
        if self.territorial_locations:
            return models.Q(
                business__territorial_location__in=self.territorial_locations
            )
        else:
            return models.Q()

    def get_value_by_territorial_locations(
        self,
        property_name: str,
    ) -> float:
        """Получение корректных числовых значений по переданным округам."""
        # Получаем территориальное расположение. Если передан список,
        # то проходимся по списку, берем все значения и берем их среднее.
        # В противном случае отдаем просто среднее значение по всем.
        if self.territorial_locations:
            average_value = 0.0
            # Из атрибута объекта берем нужную информацию по округу.
            for territorial_location in self.territorial_locations:
                average_value += getattr(territorial_location, property_name, 0.0)

            return average_value / len(self.territorial_locations)

        return getattr(self.archive, property_name, 0.0)


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
                property_name='avg_land_cadastral_value',
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
        properties = self.data.get('properties', None)
        # Если не передан размер имущества, то ищем по всем доступным. Поскольку
        # данных по имуществу нет, то переводим размер имущества в размер налога
        # на имущество.
        if properties:
            for property_name, property_value in properties[0].items():
                self.property_area += property_value
                self.type_capital_construction += (
                    f'{property_name}: {property_value}\n'
                )
            # Средняя кадастровая стоимость на имущество.
            self.avg_property_cadastral_value = self.get_value_by_territorial_locations(
                    property_name='avg_property_cadastral_value',
                )
            # Размер налога на имущество.
            self.avg_property_tax_math = (
                self.property_area *
                self.avg_property_cadastral_value *
                self.archive.property_tax_rate
            )
            # Расходны на капитальное строительство.
            self.avg_capital_construction_costs_math = (
                self.property_area *
                self.archive.avg_capital_construction_costs_math
            )

            return models.Q(
                models.Q(property_tax__gte=self.avg_property_tax_math * self.archive.lower_tax_margin_error) &
                models.Q(property_tax__lte=self.avg_property_tax_math * self.archive.upper_tax_margin_error)
            )

        return models.Q()

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

    def get_patent_costs(self) -> float:
        """Получить размер возможных налогов на патент.

        Доступно только для ИП. Для остальных лиц рассчитываем возможный доход.
        """
        avg_possible_income = 0.0
        if (
            self.data.get('need_patent') and
            self.data.get('type_business') == TypeBusiness.INDIVIDUAL
        ):
            if self.sector:

                self.avg_patent_tax = (
                    self.sector.possible_income_from_patent *
                    self.archive.patent_tax_rate
                )

                return self.avg_patent_tax

        self.avg_possible_income = self.sector.possible_income

        return 0.0

    def get_registration_costs(self) -> float:
        """Получить расходны на регистрации."""
        if self.data.get('need_registration'):
            self.avg_registration_costs = self.archive.registration_costs.get(
                self.data.get('type_business', 'other'),
                0.0,
            )

            return self.avg_registration_costs

        return 0.0

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

        return 0.0

    def get_equipment_costs(self):
        """Получение стоимости оборудования."""
        if equipments := Equipment.objects.filter(
            id__in=self.data.get('equipments', []),
        ).aggregate(
            equipment_costs=models.Sum('cost')
        ).get('equipment_costs'):
            self.equipments = equipments

            return self.equipments

        return 0.0

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
            business=business if business else None,
            # Исходные данные.
            initial_data=self.data,

            # Показатели других бизнесов, которые есть в БД.
            avg_number_of_staff_bi=avg_business_indicator.get('avg_number_of_staff'),
            avg_salary_of_staff_bi=avg_business_indicator.get('avg_salary_of_staff'),
            avg_taxes_to_the_budget_bi=avg_business_indicator.get('avg_taxes_to_the_budget'),
            avg_income_tax_bi=avg_business_indicator.get('avg_income_tax'),
            avg_property_tax_bi=avg_business_indicator.get('avg_property_tax'),
            avg_land_tax_bi=avg_business_indicator.get('avg_land_tax'),
            avg_personal_income_tax_bi=avg_business_indicator.get('avg_personal_income_tax'),
            avg_transport_tax_bi=avg_business_indicator.get('avg_transport_tax'),
            avg_other_taxes_bi=avg_business_indicator.get('avg_other_taxes'),

            # Рассчитанные показатели на основе простой математике.
            avg_number_of_staff_math=self.avg_number_of_staff,
            avg_salary_of_staff_math=self.sector.avg_salary_of_staff,
            all_salary=self.get_all_salary(),
            avg_personal_income_tax_math=self.get_avg_personal_income_tax(),

            avg_land_area_math=self.avg_land_area,
            avg_land_cadastral_value_math=self.avg_land_cadastral_value,
            avg_land_tax_math=self.avg_land_tax,

            property_area_math=self.property_area,
            avg_property_cadastral_value_math=self.avg_property_cadastral_value,
            avg_property_tax_math=self.avg_property_tax_math,
            avg_capital_construction_costs_math=self.avg_capital_construction_costs_math,
            type_capital_construction=self.type_capital_construction,

            avg_patent_tax_math=self.avg_patent_tax,
            avg_possible_income_math=self.avg_possible_income,

            # Общие расходы.
            equipment_costs=self.get_equipment_costs(),
            accounting_costs=self.get_accounting_costs(),
            registration_costs=self.get_registration_costs(),
            other_costs=self.get_other_costs(),
            other_costs_str=self.other_costs_str,

            archive=self.archive,
        )

        # Объекты в начальных данных преобразуем в слова.
        initial_data = {}
        for key_data, value_data in self.data.items():
            if key_data == 'equipments':
                initial_data.update(
                    {'equipments': [equipment.name for equipment in value_data]}
                )
            elif key_data == 'territorial_locations':
                initial_data.update(
                    {'territorial_locations': [territorial_location.full_name for territorial_location in value_data]}
                )
            else:
                initial_data.update({key_data: value_data})
        # Корректируем архив и начальные данные для успешной сериализации.
        correct_context = context.__dict__
        correct_context.update(
            {'archive': ArchiveForReportSerializer(self.archive).data},
        )
        correct_context.update(
            {'business': BaseBusinessSerializer(business).data},
        )
        correct_context.update({'initial_data': initial_data})

        self.report = Report.objects.create(
            user=self.user,
            initial_data=initial_data,
            context=correct_context,
            total_investment_amount_bi=correct_context.get('all_possible_costsbi'),
            total_investment_amount_math=correct_context.get('all_possible_costs_math'),
            sector=self.sector,
        )
        # Получение рекомендаций из ChatGPT.
        create_chat_gpt.apply_async(
            kwargs={
                'sector': self.sector.name,
                'report_id': self.report.id,
            },
        )
        # Создание тегов.
        self.create_tags()

        return self.report

    def get_all_salary(self):
        """Общий размер заработной платы."""
        self.all_salary = self.avg_number_of_staff * self.avg_salary_of_staff * 12
        return self.all_salary

    def get_avg_personal_income_tax(self):
        """Размер НДФЛ."""
        return self.all_salary * self.archive.personal_income_rate

    def get_other_costs(self):
        """Прочие общие расходы."""
        other_costs = 0
        for key_dict, value_dict in self.data.get('other').items():
            other_costs += value_dict
            self.other_costs_str += f'{key_dict}: {value_dict} тыс. руб\n'
        return other_costs

