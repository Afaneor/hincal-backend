from django.db import models
from django.utils.translation import gettext_lazy as _


class TypeBusiness(models.TextChoices):
    """Тип бизнеса: ИП, физическое лицо или компания."""

    LEGAL = 'legal', _('Юридическое лицо')
    INDIVIDUAL = 'individual', _('Индивидуальный предприниматель')
    PHYSICAL = 'physical', _('Физическое лицо')


class BusinessSector(models.TextChoices):
    """Отрасль хозяйственной деятельности"""

    FOOD_INDUSTRY = 'food_industry', _('Пищевая промышленность')
    RADIO_ELECTRONICS_AND_INSTRUMENTATION = 'radio_electronics_and_instrumentation', _('Радиоэлектроника и приборостроение')
    AVIATION_INDUSTRY = 'aviation_industry', _('Авиационная промышленность')
    AUTOMOTIVE_INDUSTRY = 'automotive_industry', _('Автомобильная промышленность')
    GENERAL_MECHANICAL_ENGINEERING = 'general_mechanical_engineering', _('Общее машиностроение')
    LIGHT_INDUSTRY = 'light_industry', _('Легкая промышленность')
    PRODUCTION_OF_PETROLEUM_PRODUCTS = 'production_of_petroleum_products', _('Производство кокса и нефтепродуктов')
    CHEMICAL_INDUSTRY = 'chemical_industry', _('Химическая промышленность')
    PRODUCTION_OF_BUILDING_MATERIALS = 'production_of_building_materials', _('Химическая промышленность')
    PRODUCTION_FOR_MILITARY = 'production_of_building_materials', _('Производство оружия, боеприпасов, спецхимии, военных машин')
    PHARMACEUTICAL_INDUSTRY = 'pharmaceutical_industry', _('Фармацевтическая промышленность')
    FUEL_AND_ENERGY_COMPLEX = 'fuel_and_energy_complex', _('Топливно-энергетический комплекс')
    MEDICAL_INDUSTRY = 'medical_industry', _('Медицинская промышленность')
    CABLE_INDUSTRY = 'cable_industry', _('Кабельная промышленность')
    WOODWORKING = 'woodworking', _('Деревообрабатывающая')
    METALLURGY_AND_METALWORKING = 'metallurgy_and_metalworking', _('Металлургия и металлообработка')
    PRINTING_ACTIVITY = 'printing_activity', _('Полиграфическая деятельность')
    PRODUCTION_OF_OTHER_CONSUMER_GOODS = 'production_of_other_consumer_goods', _('Производство прочих товаров народного потребления')
    BEVERAGE_PRODUCTION = 'beverage_production', _('Производство напитков')
    SCIENTIFIC_ACTIVITY = 'scientific_activity', _('Научная деятельность')
    MACHINE_TOOL_INDUSTRY = 'machine_tool_industry', _('Станкоинструментальная промышленность')
    SHIPBUILDING = 'shipbuilding', _('Судостроение')
    PRODUCTION_OF_RAILWAY_TRANSPORT = 'production_of_railway_transport', _('Производство ж/д транспорта')
    MANUFACTURE_OF_CONSUMER_ELECTRONICS = 'manufacture_of_consumer_electronics', _('Производство бытовой электроники и электрических приборов')
    ADDITIVE_TECHNOLOGIES = 'additive_technologies', _('Аддитивные технологии')


class BusinessSubSector(models.TextChoices):
    """Подотрасль хозяйственной деятельности"""

    DAIRY_INDUSTRY = 'dairy_industry', _('Молочная отрасль')
    INSTRUMENTATION = 'instrumentation', _('Приборостроение')
    MEAT_INDUSTRY = 'meat_industry', _('Мясная отрасль')
    CONFECTIONERY_INDUSTRY = 'confectionery_industry', _('Кондитерская отрасль')
    MANUFACTURE_OF_OTHER_GENERAL = 'manufacture_of_other_general', _('Производство прочих машин и оборудования общего назначения')
    BAKERY_INDUSTRY = 'bakery_industry', _('Хлебопекарная отрасль')
    PRODUCTION_OF_RAILWAY_TRANSPORT = 'production_of_railway_transport', _('Производство ж/д транспорта')
    FISHING_INDUSTRY = 'fishing_industry', _('Рыбная отрасль')
    PRODUCTION_OF_GENERAL_PURPOSE_EQUIPMENT = 'production_of_general_purpose_equipment', _('Производство машин и оборудования общего назначения')
    PRODUCTION_OF_CANNED_FRUITS_AND_VEGETABLES = 'production_of_canned_fruits_and_vegetables', _('Производство плодоовощных консервов')
    ELECTRICAL_ENGINEERING = 'electrical_engineering', _('Электротехника')
    PRODUCTION_OF_OTHER_SPECIAL_PURPOSE_MACHINES = 'production_of_other_special_purpose_machines', _('Производство прочих машин специального назначения')
    MACHINE_TOOL_INDUSTRY = 'machine_tool_industry', _('Станкоинструментальная промышленность')
    MICROELECTRONICS = 'microelectronics', _('Микроэлектроника')
    MILLING_AND_CEREAL_INDUSTRY = 'milling_and_cereal_industry', _('Мукомольно-крупяная отрасль')
    OTHER_INDUSTRIES = 'other_industries', _('Иные отрасли')
    BEVERAGE_PRODUCTION = 'beverage_production', _('Производство напитков')
    ANIMAL_FEED = 'animal_feed', _('Корма для животных')
    ELECTRICAL_ENGINEERING_AND_SHIPBUILDING = 'electrical_engineering_and_shipbuilding', _('Электротехника/Судостроение')
    SUGAR_INDUSTRY = 'sugar_industry', _('Сахарная отрасль')
    PRODUCTION_OF_EQUIPMENT_FOR_AGRICULTURE_AND_FORESTRY = 'production_of_equipment_for_agriculture_and_forestry', _('Производство машин и оборудования для сельского и лесного хозяйства')
    FAT_AND_OIL_INDUSTRY = 'fat_and_oil_industry', _('Масложировая отрасль')
    METALWORKING = 'metalworking', _('Металлообработка')


class TerritorialLocation(models.TextChoices):
    """Территориально расположение бизнеса по Москве (округа)."""

    WAO = 'wao', _('ВАО')
    ZAO = 'zao', _('ЗАО')
    ZELAO = 'zelao', _('ЗелАО')
    NAO = 'nao', _('НАО')
    SAO = 'sao', _('САО')
    SWAO = 'swao', _('СВАО')
    SZAO = 'szao', _('СЗАО')
    TAO = 'tao', _('ТАО')
    CAO = 'cao', _('ЦАО')
    YUAO = 'yuao', _('ЮАО')
    YUWAO = 'yuwao', _('ЮВАО')
    YUZAO = 'yuzao', _('ЮЗАО')
    OTHER = 'other', _('Другое')
