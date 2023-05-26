import datetime
from dataclasses import dataclass, field

from server.apps.hincal.models import Archive, Business, Equipment
from server.apps.hincal.services.enums import TypeTaxSystem


def get_correct_data(entity, property_name):
    """Получение корректного значения."""
    if value := getattr(entity, property_name, None):
        return value
    return 'Данные не предоставлены'


@dataclass()
class ReportContextDataClass:
    """Дата класс контекста отчета."""

    # Дата формирования отчета.
    create_date: str = str(datetime.datetime.now())
    # Информация о бизнесе.
    business: Business = None
    # Исходные данные, которые ввел пользователь в калькуляторе.
    initial_data: dict = None

    # Генерация текста из ChatGPT.
    chat_gpt_page_2: str = ''
    chat_gpt_page_3: str = ''
    chat_gpt_page_4: str = ''
    chat_gpt_page_5: str = ''
    chat_gpt_page_6: str = ''
    chat_gpt_page_7: str = ''
    chat_gpt_page_8: str = ''

    # Средние показатели расходов по другим бизнесам, которые есть в БД.
    avg_number_of_staff_bi: float = 0
    avg_salary_of_staff_bi: float = 0
    avg_taxes_to_the_budget_bi: float = 0
    avg_income_tax_bi: float = 0
    avg_property_tax_bi: float = 0
    avg_land_tax_bi: float = 0
    avg_personal_income_tax_bi: float = 0
    avg_transport_tax_bi: float = 0
    avg_other_taxes_bi: float = 0

    # Рассчитанные показатели расходов на основе математики.
    # Расходы по персоналу.
    avg_number_of_staff_math: float = 0
    avg_salary_of_staff_math: float = 0
    all_salary: float = 0
    avg_personal_income_tax_math: float = 0

    # Расходы по земле.
    avg_land_area_math: float = 0
    avg_land_cadastral_value_math: float = 0
    avg_land_tax_math: float = 0

    # Расходы по имуществу.
    avg_property_area_math: float = 0
    avg_property_cadastral_value_math: float = 0
    avg_property_tax_math: float = 0

    # Средний размер налога на патент.
    avg_patent_tax_math: float = 0
    # Возможный доход предприятия по сектору.
    avg_possible_income_math: float = 0

    # Расходы на оборудование.
    equipment_costs: float = 0
    # Расходы на бухгалтерские услуги.
    accounting_costs: float = 0
    # Расходы на регистрацию.
    registration_costs: float = 0

    # ВЫЧИСЛЯЕМЫЕ ПОЛЯ.
    # Итоговые возможные расходы по всему.
    all_possible_costs_db: float = field(init=False)
    all_possible_costs_math: float = field(init=False)
    # Общие расходны на сотрудников.
    all_staff_costs: float = field(init=False)
    # Общие расходны на аренду земли и объектов недвижимости.
    all_lp_lease_costs: float = field(init=False)
    # Общие налоги на сотрудников, землю и объекты недвижимости.
    all_tax_costs: float = field(init=False)
    # Общие расходы на услуги.
    all_services_costs: float = field(init=False)

    avg_income_tax_math: float = field(init=False)

    # Расходы на з.п./налоги/взносы персонала.
    avg_staff_tax_costs: float = field(init=False)
    avg_staff_pension_contributions_costs: float = field(init=False)
    avg_staff_medical_contributions_costs: float = field(init=False)

    # Расходы аренды/покупки земли.
    avg_land_lease_costs: float = field(init=False)
    avg_land_purchase_costs: float = field(init=False)

    context_for_file: dict = field(init=False)

    archive: Archive = None

    def __post_init__(self):
        """Рассчитываем недостающие показатели."""
        # СТРАНИЦА 4.
        # Отчисления в ПФР согласно данным из БД.
        self.avg_staff_pension_contributions_costs_bi = (
            self.avg_number_of_staff_bi *
            self.avg_salary_of_staff_bi *
            self.archive.pension_contributions_rate
        )
        # Отчисления в ФМС согласно данным из БД.
        self.avg_staff_medical_contributions_costs_bi = (
            self.avg_number_of_staff_bi *
            self.avg_salary_of_staff_bi *
            self.archive.medical_contributions_rate
        )
        # Отчисления по нетрудоспособности согласно данным из БД.
        self.avg_staff_disability_contributions_costs_bi = (
            self.avg_number_of_staff_bi *
            self.avg_salary_of_staff_bi *
            self.archive.disability_contributions_rate
        )

        # Все расходы: з.п. сотрудников + НДФЛ +страховые взносы +
        # налог на прибыль, землю, имущество, транспорт, другие налоги,
        # патентную систему, бухгалтерию, оборудование, регистрацию.
        # FIXME налог уплачивается на год. А расходы на зп, бух. учет. на месяц
        self.all_possible_costs_db = (
            self.avg_salary_of_staff_bi +
            self.avg_personal_income_tax_bi +
            self.avg_staff_pension_contributions_costs_bi +
            self.avg_staff_medical_contributions_costs_bi +
            self.avg_staff_disability_contributions_costs_bi +
            self.avg_income_tax_bi +
            self.avg_property_tax_bi +
            self.avg_land_tax_bi +
            self.avg_transport_tax_bi +
            self.avg_other_taxes_bi +
            self.equipment_costs +
            self.accounting_costs +
            self.registration_costs
        )
        # Все расходы на сотрудника: з.п. сотрудников + НДФЛ + страховые взносы
        self.all_staff_costs_bi = (
            self.avg_salary_of_staff_bi +
            self.avg_personal_income_tax_bi +
            self.avg_staff_pension_contributions_costs_bi +
            self.avg_staff_medical_contributions_costs_bi +
            self.avg_staff_disability_contributions_costs_bi
        )
        # Все расходы на землю и имущество: налог на землю, налог на имущество,
        # налог на транспорт.
        self.all_lp_lease_costs_bi = (
            self.avg_property_tax_bi +
            self.avg_land_tax_bi +
            self.avg_transport_tax_bi
        )
        # Все расходы на налоги.
        self.all_tax_costs_bi = (
            self.avg_personal_income_tax_bi +
            self.avg_income_tax_bi +
            self.avg_property_tax_bi +
            self.avg_land_tax_bi +
            self.avg_transport_tax_bi +
            self.avg_other_taxes_bi
        )
        # Все расходы на сервисы.
        self.all_services_costs_bi = (
            self.accounting_costs +
            self.registration_costs
        )

        # ОБЩИЕ РАСХОДЫ СОГЛАСНО МАТЕМАТИКЕ.
        # Отчисления в ПФР согласно расчетам.
        self.avg_staff_pension_contributions_costs_math = (
            self.avg_number_of_staff_math *
            self.avg_salary_of_staff_math *
            self.archive.pension_contributions_rate
        )
        # Отчисления в ФМС согласно расчетам.
        self.avg_staff_medical_contributions_costs_math = (
            self.avg_number_of_staff_math *
            self.avg_salary_of_staff_math *
            self.archive.medical_contributions_rate
        )
        # Отчисления по нетрудоспособности согласно данным из БД.
        self.avg_staff_disability_contributions_costs_math = (
            self.avg_number_of_staff_math *
            self.avg_salary_of_staff_math *
            self.archive.disability_contributions_rate
        )

        # Расчет налога на прибыль.
        if self.avg_patent_tax_math:
            self.avg_income_tax_math = self.avg_patent_tax_math
        elif self.business and self.business.type_tax_system == TypeTaxSystem.OSN:
            self.avg_income_tax_math = (
                self.avg_possible_income_math *
                self.archive.osn_tax_rate
            )
        elif self.business and self.business.type_tax_system == TypeTaxSystem.YSN:
            self.avg_income_tax_math = (
                self.avg_possible_income_math *
                self.archive.ysn_tax_rate
            )
        elif self.business is None:
            self.avg_income_tax_math = (
                self.avg_possible_income_math *
                self.archive.osn_tax_rate
            )
        else:
            self.avg_income_tax_math = 0.0

        self.all_possible_costs_math = (
            self.avg_salary_of_staff_math +
            self.avg_personal_income_tax_math +
            self.avg_staff_pension_contributions_costs_math +
            self.avg_staff_medical_contributions_costs_math +
            self.avg_staff_disability_contributions_costs_math +
            self.avg_income_tax_math +
            self.avg_property_tax_math +
            self.avg_land_tax_math +
            self.equipment_costs +
            self.accounting_costs +
            self.registration_costs
        )

        # Все расходы на сотрудника: з.п. сотрудников + НДФЛ + страховые взносы
        self.all_staff_costs_math = (
            self.avg_salary_of_staff_math +
            self.avg_personal_income_tax_math +
            self.avg_staff_pension_contributions_costs_math +
            self.avg_staff_medical_contributions_costs_math +
            self.avg_staff_disability_contributions_costs_math
        )
        # Все расходы на землю и имущество: налог на землю, налог на имущество,
        # налог на транспорт.
        self.all_lp_lease_costs_math = (
            self.avg_property_tax_math +
            self.avg_land_tax_math
        )
        # Все расходы на налоги.
        self.all_tax_costs_math = (
            self.avg_personal_income_tax_math +
            self.avg_income_tax_math +
            self.avg_property_tax_math +
            self.avg_land_tax_math
        )

        # Все расходы на сервисы.
        self.all_services_costs_math = (
            self.accounting_costs +
            self.registration_costs
        )

        # СТРАНИЦА 5.
        # Стоимость покупки/аренды имущества.
        avg_property_lease_costs = 0.0
        avg_property_purchase_costs = 0.0
        # Стоимость покупки/аренды земли.
        avg_land_lease_costs = 0.0
        avg_land_purchase_costs = 0.0

        territorial_locations = self.initial_data.get('territorial_locations')
        len_territorial_locations = len(territorial_locations) if len(territorial_locations) != 0 else 1
        if territorial_locations:
            for territorial_location in territorial_locations:
                avg_property_lease_costs += territorial_location.avg_property_lease_costs
                avg_property_purchase_costs += territorial_location.avg_property_purchase_costs
                avg_land_lease_costs += territorial_location.avg_land_lease_costs
                avg_land_purchase_costs += territorial_location.avg_land_purchase_costs
        else:
            avg_property_lease_costs += self.archive.avg_property_lease_costs
            avg_property_purchase_costs += self.archive.avg_property_purchase_costs
            avg_land_lease_costs += self.archive.avg_land_lease_costs
            avg_land_purchase_costs += self.archive.avg_land_purchase_costs

        # Средняя стоимость аренды/покупки квадратного метра имущества.
        self.avg_property_lease_value = (
            avg_property_lease_costs / len_territorial_locations
        )
        self.avg_property_purchase_value = (
            avg_property_purchase_costs / len_territorial_locations
        )
        # Средняя стоимость аренды/покупки квадратного метра земли.
        self.avg_land_lease_value = (
            avg_land_lease_costs / len_territorial_locations
        )
        self.avg_land_purchase_value = (
            avg_land_purchase_costs / len_territorial_locations
        )

        # Страница 6.
        data_by_equipments = ''
        all_equipment_coasts = 0.0
        if self.equipment_costs:
            equipments = Equipment.objects.filter(
                id__in=self.initial_data.get('equipments', []),
            )
        else:
            if self.business:
                tags = [
                    self.business.sector,
                    self.business.sub_sector,
                    self.business.type,
                    self.business.okved,
                ]
            else:
                tags = ['all']
            equipments = Equipment.objects.filter(
                tags__name__in=tags,
            )

        for en_index, equipment in enumerate(equipments):
            if en_index < 5:
                data_by_equipments += f'{equipment.name} -- {equipment.cost}\n'
            all_equipment_coasts += equipment.cost
        data_by_equipments += f'Общая сумма оборудования: {all_equipment_coasts} тыс. руб.\n'

        if self.business:
            indicator = self.business.business_indicators.first()
        else:
            indicator = None
        self.context_for_file = {
            # ИНФОРМАЦИЯ О ВАШЕЙ ОРГАНИЗАЦИИ.
            'sector': get_correct_data(self.business, 'sector'),
            'full_opf': get_correct_data(self.business, 'full_opf'),
            'number_of_staff':
                get_correct_data(indicator, 'average_number_of_staff'),
            'territorial_location':
                get_correct_data(self.business, 'territorial_location'),
            'type_tax_system':
                get_correct_data(self.business, 'type_tax_system'),
            'land_area': get_correct_data(indicator, 'land_area'),
            'building_area': get_correct_data(indicator, 'building_area'),

            # Слова ищ ChatGpt.
            'chat_gpt_page_3': self.chat_gpt_page_3,
            'chat_gpt_page_4': self.chat_gpt_page_4,
            'chat_gpt_page_5': self.chat_gpt_page_5,
            'chat_gpt_page_6': self.chat_gpt_page_6,
            'chat_gpt_page_7': self.chat_gpt_page_7,
            'chat_gpt_page_8': self.chat_gpt_page_8,

            # ИТОГОВЫЕ ЗНАЧЕНИЯ ВОЗМОЖНЫХ ЗАТРАТ НА ОСНОВЕ БД.
            'all_possible_costs_bi': self.all_possible_costs_db,
            'all_staff_costs_bi': self.all_staff_costs_bi,
            'all_lp_lease_costs_bi': self.all_lp_lease_costs_bi,
            'equipment_costs_bi': self.equipment_costs,
            'all_tax_costs_bi': self.all_tax_costs_bi,
            'all_services_costs_bi': self.all_services_costs_bi,

            # ИТОГОВЫЕ ЗНАЧЕНИЯ ВОЗМОЖНЫХ ЗАТРАТ НА ОСНОВЕ МАТЕМАТИКИ.
            'all_possible_costs_math': self.all_possible_costs_math,
            'all_staff_costs_math': self.all_staff_costs_math,
            'all_lp_lease_costs_math': self.all_lp_lease_costs_math,
            'equipment_costs_math': self.equipment_costs,
            'all_tax_costs_math': self.all_services_costs_math,
            'all_services_costs_math': self.all_services_costs_math,

            # 4 Страница. Анализ расходов на персонал.
            # ИТОГОВЫЕ ЗНАЧЕНИЯ ЗАТРАТ НА ПЕРСОНАЛ НА ОСНОВЕ БД.
            'avg_salary_of_staff_bi': self.all_staff_costs_bi,
            'avg_personal_income_tax_bi': self.all_lp_lease_costs_bi,
            'avg_staff_pension_contributions_costs_bi': self.equipment_costs,
            'avg_staff_medical_contributions_costs_bi': self.all_tax_costs_bi,
            'avg_staff_disability_contributions_costs_bi': self.all_services_costs_bi,

            # ИТОГОВЫЕ ЗНАЧЕНИЯ ЗАТРАТ НА ПЕРСОНАЛ НА ОСНОВЕ МАТЕМАТИКИ.
            'avg_salary_of_staff_math': self.all_staff_costs_math,
            'avg_personal_income_tax_math': self.all_lp_lease_costs_math,
            'avg_staff_pension_contributions_costs_math': self.equipment_costs,
            'avg_staff_medical_contributions_costs_math': self.all_services_costs_math,
            'avg_staff_disability_contributions_costs_math': self.all_services_costs_math,

            # 5 Страница. Сравнение цен имущества в аренду и в покупку.
            # Диапазон площади.
            'property_range': f"{self.initial_data.get('from_property_area')} - {self.initial_data.get('to_property_area')}",
            'land_range': f"{self.initial_data.get('from_land_area')} - {self.initial_data.get('to_land_area')}",
            
            # Стоимость кв.м. аренды имущества.
            'avg_property_lease_value': self.avg_property_lease_value,
            # Общие расходы по аренде имущества.
            'all_property_lease_costs': self.avg_property_lease_value * self.avg_property_area_math,
            
            # Стоимость кв.м. покупки.
            'avg_property_purchase_value': self.avg_property_purchase_value,
            # Налог на недвижимость.
            'avg_property_tax': self.avg_property_tax_math,
            # Общие расходы по покупке имущества.
            'all_property_purchase_costs': (
                self.avg_property_purchase_value * 
                self.avg_property_area_math + 
                self.avg_property_tax_math
            ),

            # Стоимость кв.м. аренды земли.
            'avg_land_lease_value': self.avg_land_lease_value,
            # Общие расходы по аренде земли.
            'all_land_lease_costs': self.avg_land_lease_value * self.avg_land_area_math,

            # Стоимость кв.м. покупки земли.
            'avg_land_purchase_value': self.avg_land_purchase_value,
            # Налог на землю.
            'avg_land_tax': self.avg_land_tax_math,
            # Общие расходы по покупке земли.
            'all_land_purchase_costs': (
                self.avg_land_purchase_value *
                self.avg_land_area_math +
                self.avg_land_tax_math
            ),

            # 6 Страница. Возможные неучитываемые расходы.
            # Предложить оборудование.
            'equipments': data_by_equipments,

            # 7 Страница. Предложения по бизнесу (исходя из сферы).
        }
