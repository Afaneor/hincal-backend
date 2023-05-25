import datetime
from dataclasses import dataclass, field

from server.apps.hincal.models import Archive


@dataclass()
class ReportContextDataClass:
    """Дата класс контекста отчета."""

    # Дата формирования отчета.
    create_date: str = str(datetime.datetime.now())
    # Информация о бизнесе.
    business: dict = None
    # Исходные данные.
    initial_data: dict = None

    # Генерация текста из ChatGPT.
    chat_gpt_page_2: str = ''
    chat_gpt_page_3: str = ''
    chat_gpt_page_4: str = ''
    chat_gpt_page_5: str = ''
    chat_gpt_page_6: str = ''
    chat_gpt_page_7: str = ''
    chat_gpt_page_8: str = ''

    # рассчитанные показатели расходов.
    avg_number_of_staff_math: float = 0
    avg_salary_of_staff_math: float = 0
    avg_personal_income_tax_math: float = 0
    avg_taxes_to_the_subject_budget_math: float = 0
    avg_taxes_to_the_federal_budget_math: float = 0
    avg_property_tax_math: float = 0
    avg_land_tax_math: float = 0

    # Итоговые возможные расходы по всему.
    all_possible_costs: float = field(init=False)
    # Общие расходны на сотрудников.
    all_staff_costs: float = field(init=False)
    # Общие расходны на аренду земли и объектов недвижимости.
    all_lp_lease_costs: float = field(init=False)
    # Общие расходны на покупку земли и объектов недвижимости.
    all_lp_purchase_costs: float = field(init=False)
    # Общие расходны на налоги по земле и объектам недвижимости.
    all_lp_tax_costs: float = field(init=False)
    # Общие налоги на сотрудников, землю и объекты недвижимости.
    all_tax_costs: float = field(init=False)
    # Общие расходы на услуги.
    all_services_costs: float = field(init=False)

    # Средние показатели расходов.
    # Расходы по персоналу.
    avg_number_of_staff_by_indicators: float = 0
    avg_salary_of_staff_by_indicators: float = 0
    avg_taxes_to_the_budget_by_indicators: float = 0
    avg_income_tax_by_indicators: float = 0
    avg_property_tax_by_indicators: float = 0
    avg_land_tax_by_indicators: float = 0
    avg_personal_income_tax_by_indicators: float = 0
    avg_transport_tax_by_indicators: float = 0
    avg_other_taxes_by_indicators: float = 0

    # Расходы на оборудование.
    equipment_costs: float = 0
    # Расходы на бухгалтерские услуги.
    accounting_costs: float = 0
    # Расходы на регистрацию.
    registration_costs: float = 0

    # Расходы на з.п./налоги/взносы персонала.'
    avg_staff_tax_costs: float = field(init=False)
    avg_staff_pension_contributions_costs: float = field(init=False)
    avg_staff_medical_contributions_costs: float = field(init=False)

    # Расходы аренды/покупки земли.
    avg_land_lease_costs: float = field(init=False)
    avg_land_purchase_costs: float = field(init=False)

    # Расходы аренды/покупки/ремонта на объекты недвижимости.
    building_lease_costs: float = field(init=False)
    building_purchase_costs: float = field(init=False)
    building_repair_costs: float = field(init=False)

    archive: Archive = None

    def __post_init__(self):
        # Расходы на налоги/взносы персонала. Размер налогов уже включен в з/п.
        self.avg_staff_tax_costs = (
            self.avg_number_of_staff_by_indicators *
            self.avg_salary_of_staff_by_indicators *
            self.archive.personal_income_rate
        )
        self.avg_staff_pension_contributions_costs = (
            self.avg_number_of_staff_by_indicators *
            self.avg_salary_of_staff_by_indicators *
            self.archive.pension_contributions_rate
        )
        self.avg_staff_medical_contributions_costs = (
            self.avg_number_of_staff_by_indicators *
            self.avg_salary_of_staff_by_indicators *
            self.archive.medical_contributions_rate
        )

        # Расходы аренды/покупки земли.
        land_area = self.avg_land_tax_by_indicators / self.archive.land_tax_rate
        self.avg_land_lease_costs = (
            land_area * self.archive.avg_land_lease_costs
        )
        self.avg_land_purchase_costs = (
            land_area * self.archive.avg_land_purchase_costs
        )

        # Расходы аренды/покупки/ремонта на объекты недвижимости.
        property_area = self.avg_property_tax_by_indicators / self.archive.property_tax_rate
        self.property_lease_costs = (
            property_area * self.archive.avg_property_lease_costs
        )
        self.property_purchase_costs = (
            property_area * self.archive.avg_property_purchase_costs
        )
        self.property_repair_costs = (
            property_area * self.archive.avg_property_repair_costs
        )

        # Итоговые возможные расходы по всему.
        self.all_possible_costs = (
            self.avg_number_of_staff_by_indicators +
            self.avg_salary_of_staff_by_indicators +
            self.avg_taxes_to_the_budget_by_indicators +
            self.avg_income_tax_by_indicators +
            self.avg_property_tax_by_indicators +
            self.avg_land_tax_by_indicators +
            self.avg_personal_income_tax_by_indicators +
            self.avg_transport_tax_by_indicators +
            self.avg_other_taxes_by_indicators +
            self.avg_staff_pension_contributions_costs +
            self.avg_staff_medical_contributions_costs +
            self.avg_land_lease_costs +
            self.property_lease_costs +
            self.equipment_costs +
            self.accounting_costs +
            self.registration_costs
        )
        # Общие расходны на сотрудников.
        self.all_staff_costs = (
            self.avg_salary_of_staff_by_indicators +
            self.avg_staff_pension_contributions_costs +
            self.avg_staff_medical_contributions_costs
        )
        # Общие расходны на аренду земли и объектов недвижимости.
        self.all_lp_lease_costs = (
            self.avg_land_lease_costs +
            self.property_lease_costs +
            self.property_repair_costs
        )
        # Общие расходны на покупку земли и объектов недвижимости.
        self.all_lp_purchase_costs = (
            self.avg_land_purchase_costs +
            self.property_lease_costs +
            self.property_repair_costs
        )
        # Общие расходны на налоги по земле и объектам недвижимости.
        self.all_lp_tax_costs = (
            self.avg_property_tax_by_indicators +
            self.avg_land_tax_by_indicators
        )
        # Общие расходы на сотрудников, аренду земли и объекты недвижимости.
        self.all_staff_and_lease_lp_costs = (
            self.all_staff_costs +
            self.all_lp_lease_costs
        )
        # Общие расходы на сотрудников, покпку земли и объекты недвижимости.
        self.all_staff_and_lease_lp_costs = (
            self.all_staff_costs +
            self.all_lp_purchase_costs
        )
        # Общие расходы на услуги.
        self.all_services_costs =(
            self.accounting_costs
        )
