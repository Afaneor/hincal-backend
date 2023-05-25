import xlrd
from django.core.management.base import BaseCommand
from server.apps.hincal.models import Indicator, Business
from server.apps.hincal.services.enums import BusinessSector, BusinessSubSector

BUSINESS_SECTOR = {
    'Пищевая промышленность': BusinessSector.FOOD_INDUSTRY,
    'Радиоэлектроника и приборостроение': BusinessSector.RADIO_ELECTRONICS_AND_INSTRUMENTATION,
    'Авиационная промышленность': BusinessSector.AVIATION_INDUSTRY,
    'Автомобильная промышленность': BusinessSector.AUTOMOTIVE_INDUSTRY,
    'Общее машиностроение (в т.ч. оборудование пищевой переработки, дорожногстроительная и сельскохозяйственная техника)': BusinessSector.GENERAL_MECHANICAL_ENGINEERING,
    'Легкая промышленность': BusinessSector.LIGHT_INDUSTRY,
    'Производство кокса и нефтепродуктов': BusinessSector.PRODUCTION_OF_PETROLEUM_PRODUCTS,
    'Химическая промышленность': BusinessSector.CHEMICAL_INDUSTRY,
    'Производство строительных материалов': BusinessSector.PRODUCTION_OF_BUILDING_MATERIALS,
    'Производство оружия, боеприпасов, спецхимии, военных машин': BusinessSector.PRODUCTION_FOR_MILITARY,
    'Фармацевтическая промышленность': BusinessSector.PHARMACEUTICAL_INDUSTRY,
    'Топливно-энергетический комплекс': BusinessSector.FUEL_AND_ENERGY_COMPLEX,
    'Медицинская промышленность': BusinessSector.MEDICAL_INDUSTRY,
    'Кабельная промышленность': BusinessSector.CABLE_INDUSTRY,
    'Деревообрабатывающая': BusinessSector.WOODWORKING,
    'Металлургия и металлообработка': BusinessSector.METALLURGY_AND_METALWORKING,
    'Полиграфическая деятельность': BusinessSector.PRINTING_ACTIVITY,
    'Производство прочих товаров народного потребления': BusinessSector.PRODUCTION_OF_OTHER_CONSUMER_GOODS,
    'Производство напитков': BusinessSector.BEVERAGE_PRODUCTION,
    'Научная деятельность': BusinessSector.SCIENTIFIC_ACTIVITY,
    'Станкоинструментальная промышленность': BusinessSector.MACHINE_TOOL_INDUSTRY,
    'Судостроение': BusinessSector.SHIPBUILDING,
    'Производство ж/д транспорта': BusinessSector.PRODUCTION_OF_RAILWAY_TRANSPORT,
    'Производство бытовой электроники и электрических приборов': BusinessSector.MANUFACTURE_OF_CONSUMER_ELECTRONICS,
    'Аддитивные технологии': BusinessSector.ADDITIVE_TECHNOLOGIES,
}

BUSINESS_SUB_SECTOR = {
    'Молочная отрасль': BusinessSubSector.DAIRY_INDUSTRY,
    'Приборостроение': BusinessSubSector.INSTRUMENTATION,
    'Мясная отрасль': BusinessSubSector.MEAT_INDUSTRY,
    'Сведения отсутствуют': BusinessSubSector.OTHER,
    'Кондитерская отрасль': BusinessSubSector.CONFECTIONERY_INDUSTRY,
    'Производство прочих машин и оборудования общего назначения': BusinessSubSector.MANUFACTURE_OF_OTHER_GENERAL,
    'Хлебопекарная отрасль': BusinessSubSector.BAKERY_INDUSTRY,
    'Производство ж/д транспорта': BusinessSubSector.PRODUCTION_OF_RAILWAY_TRANSPORT,
    'Рыбная отрасль': BusinessSubSector.FISHING_INDUSTRY,
    'Производство машин и оборудования общего назначения': BusinessSubSector.PRODUCTION_OF_GENERAL_PURPOSE_EQUIPMENT,
    'Производство плодоовощных консервов': BusinessSubSector.PRODUCTION_OF_CANNED_FRUITS_AND_VEGETABLES,
    'Электротехника': BusinessSubSector.ELECTRICAL_ENGINEERING,
    'Производство прочих машин специального назначения': BusinessSubSector.PRODUCTION_OF_OTHER_SPECIAL_PURPOSE_MACHINES,
    'Станкоинструментальная промышленность': BusinessSubSector.MACHINE_TOOL_INDUSTRY,
    'Микроэлектроника': BusinessSubSector.MICROELECTRONICS,
    'Мукомольно-крупяная отрасль': BusinessSubSector.MILLING_AND_CEREAL_INDUSTRY,
    'Иные отрасли': BusinessSubSector.OTHER,
    'Производство напитков': BusinessSubSector.BEVERAGE_PRODUCTION,
    'Корма для животных': BusinessSubSector.ANIMAL_FEED,
    'Электротехника/Судостроение': BusinessSubSector.ELECTRICAL_ENGINEERING_AND_SHIPBUILDING,
    'Сахарная отрасль': BusinessSubSector.SUGAR_INDUSTRY,
    'Производство машин и оборудования для сельского и лесного хозяйства': BusinessSubSector.PRODUCTION_OF_EQUIPMENT_FOR_AGRICULTURE_AND_FORESTRY,
    'Масложировая отрасль': BusinessSubSector.FAT_AND_OIL_INDUSTRY,
    'Металлообработка': BusinessSubSector.METALWORKING,
}


class Command(BaseCommand):
    """Добавление данных в Indicator"""

    help = 'Добавление данных в Indicator'

    def handle(self, *args, **options):  # noqa: WPS110
        """Добавление данных в Indicator"""
        workbook = xlrd.open_workbook('server/apps/hincal/management/commands/data.xls')
        worksheet = workbook.sheet_by_index(0)

        # Iterate the rows and columns
        indicators = []
        for i in range(1, 3529):
            business = Business.objects.create(
                sector=BUSINESS_SECTOR.get(worksheet.cell_value(i, 0)),
                sub_sector=BUSINESS_SUB_SECTOR.get(worksheet.cell_value(i, 1)),
            )
            indicators.append(
                Indicator(
                    business=business,
                    year=2021,
                    average_number_of_staff=float(worksheet.cell_value(i, 3)),
                    average_salary_of_staff=float(worksheet.cell_value(i, 5)),
                    taxes_to_the_budget=float(worksheet.cell_value(i, 7)),
                    income_tax=float(worksheet.cell_value(i, 9)),
                    property_tax=float(worksheet.cell_value(i, 11)),
                    land_tax=float(worksheet.cell_value(i, 13)),
                    personal_income_tax=float(worksheet.cell_value(i, 15)),
                    transport_tax=float(worksheet.cell_value(i, 17)),
                    other_taxes=float(worksheet.cell_value(i, 19)),
                ),
            )
            indicators.append(
                Indicator(
                    business=business,
                    year=2022,
                    average_number_of_staff=float(worksheet.cell_value(i, 2)),
                    average_salary_of_staff=float(worksheet.cell_value(i, 4)),
                    taxes_to_the_budget=float(worksheet.cell_value(i, 6)),
                    income_tax=float(worksheet.cell_value(i, 8)),
                    property_tax=float(worksheet.cell_value(i, 10)),
                    land_tax=float(worksheet.cell_value(i, 12)),
                    personal_income_tax=float(worksheet.cell_value(i, 14)),
                    transport_tax=float(worksheet.cell_value(i, 16)),
                    other_taxes=float(worksheet.cell_value(i, 18)),
                ),
            )
            print(f'Обработана строка № {i}')
        Indicator.objects.bulk_create(indicators)
