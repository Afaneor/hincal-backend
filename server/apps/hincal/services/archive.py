from dataclasses import dataclass

from server.apps.hincal.services.enums import BusinessSector, TypeBusiness


def get_land_cadastral_value():
    """Обертка для сохранения информации в поле модели."""
    return LandCadastralValue().data


def get_property_cadastral_value():
    """Обертка для сохранения информации в поле модели."""
    return PropertyCadastralValue().data


def get_cost_accounting():
    """Обертка для сохранения информации в поле модели."""
    return CostAccounting().data


def get_possible_income_from_patent():
    """Обертка для сохранения информации в поле модели."""
    return PossibleIncomeFromPatent().data


def get_registration_costs():
    """Обертка для сохранения информации в поле модели."""
    return RegistrationCosts().data


def get_average_salary():
    """Обертка для сохранения информации в поле модели."""
    return AverageSalary().data

@dataclass
class LandCadastralValue:
    """Данные по кадастровой стоимости земли, тыс. руб."""

    data = {
        'wao': 15.49236,
        'zao': 11.70322,
        'zelao': 4.1115,
        'nao': 5.33394,
        'sao': 20.53299,
        'swao': 19.48533,
        'szao': 19.96159,
        'tao': 28.9051,
        'cao': 63.27479,
        'yuao': 13.51037,
        'yuwao': 14.08697,
        'yuzao': 16.4231,
        'other': 17.23389,
    }


@dataclass
class PropertyCadastralValue:
    """Данные по кадастровой стоимости имущества, тыс. руб."""

    data = {
        'wao': 15.49236,
        'zao': 11.70322,
        'zelao': 4.1115,
        'nao': 5.33394,
        'sao': 20.53299,
        'swao': 19.48533,
        'szao': 19.96159,
        'tao': 28.9051,
        'cao': 63.27479,
        'yuao': 13.51037,
        'yuwao': 14.08697,
        'yuzao': 16.4231,
        'other': 17.23389,
    }


@dataclass
class CostAccounting:
    """Данные по ведению бухгалтерского учета, тыс. руб."""

    data = {
        'legal': {
            'osn': {
                'lower': 9,
                'upper': 40,
            },
            'ysn': {
                'lower': 7,
                'upper': 30,
            },
            'patent': {
                'lower': 0,
                'upper': 0,
            },
        },
        'individual': {
            'osn': {
                'lower': 6,
                'upper': 35,
            },
            'ysn': {
                'lower': 5,
                'upper': 25,
            },
            'patent': {
                'lower': 5,
                'upper': 25,
            },
        },

    }


@dataclass
class PossibleIncomeFromPatent:
    """Возможный доход по патентной системе, тыс. руб. Закон № 53."""

    data = {
        BusinessSector.FOOD_INDUSTRY: 10000,
        BusinessSector.RADIO_ELECTRONICS_AND_INSTRUMENTATION: 10000,
        BusinessSector.AVIATION_INDUSTRY: 10000,
        BusinessSector.AUTOMOTIVE_INDUSTRY: 10000,
        BusinessSector.GENERAL_MECHANICAL_ENGINEERING: 10000,
        BusinessSector.LIGHT_INDUSTRY: 10000,
        BusinessSector.PRODUCTION_OF_PETROLEUM_PRODUCTS: 10000,
        BusinessSector.CHEMICAL_INDUSTRY: 10000,
        BusinessSector.PRODUCTION_OF_BUILDING_MATERIALS: 10000,
        BusinessSector.PRODUCTION_FOR_MILITARY: 10000,
        BusinessSector.PHARMACEUTICAL_INDUSTRY: 10000,
        BusinessSector.FUEL_AND_ENERGY_COMPLEX: 10000,
        BusinessSector.MEDICAL_INDUSTRY: 10000,
        BusinessSector.CABLE_INDUSTRY: 10000,
        BusinessSector.WOODWORKING: 10000,
        BusinessSector.METALLURGY_AND_METALWORKING: 10000,
        BusinessSector.PRINTING_ACTIVITY: 10000,
        BusinessSector.PRODUCTION_OF_OTHER_CONSUMER_GOODS: 10000,
        BusinessSector.BEVERAGE_PRODUCTION: 10000,
        BusinessSector.SCIENTIFIC_ACTIVITY: 10000,
        BusinessSector.MACHINE_TOOL_INDUSTRY: 10000,
        BusinessSector.SHIPBUILDING: 10000,
        BusinessSector.PRODUCTION_OF_RAILWAY_TRANSPORT: 10000,
        BusinessSector.MANUFACTURE_OF_CONSUMER_ELECTRONICS: 10000,
        BusinessSector.OTHER: 10000,
    }


@dataclass
class RegistrationCosts:
    """Расходы на регистрацию, тыс. руб."""

    data = {
        TypeBusiness.LEGAL: 40,
        TypeBusiness.INDIVIDUAL: 0.8,
    }


@dataclass
class AverageSalary:
    """Размер средней заработной платы по секторам, тыс. руб."""

    data = {
        BusinessSector.FOOD_INDUSTRY: 10000,
        BusinessSector.RADIO_ELECTRONICS_AND_INSTRUMENTATION: 10000,
        BusinessSector.AVIATION_INDUSTRY: 10000,
        BusinessSector.AUTOMOTIVE_INDUSTRY: 10000,
        BusinessSector.GENERAL_MECHANICAL_ENGINEERING: 10000,
        BusinessSector.LIGHT_INDUSTRY: 10000,
        BusinessSector.PRODUCTION_OF_PETROLEUM_PRODUCTS: 10000,
        BusinessSector.CHEMICAL_INDUSTRY: 10000,
        BusinessSector.PRODUCTION_OF_BUILDING_MATERIALS: 10000,
        BusinessSector.PRODUCTION_FOR_MILITARY: 10000,
        BusinessSector.PHARMACEUTICAL_INDUSTRY: 10000,
        BusinessSector.FUEL_AND_ENERGY_COMPLEX: 10000,
        BusinessSector.MEDICAL_INDUSTRY: 10000,
        BusinessSector.CABLE_INDUSTRY: 10000,
        BusinessSector.WOODWORKING: 10000,
        BusinessSector.METALLURGY_AND_METALWORKING: 10000,
        BusinessSector.PRINTING_ACTIVITY: 10000,
        BusinessSector.PRODUCTION_OF_OTHER_CONSUMER_GOODS: 10000,
        BusinessSector.BEVERAGE_PRODUCTION: 10000,
        BusinessSector.SCIENTIFIC_ACTIVITY: 10000,
        BusinessSector.MACHINE_TOOL_INDUSTRY: 10000,
        BusinessSector.SHIPBUILDING: 10000,
        BusinessSector.PRODUCTION_OF_RAILWAY_TRANSPORT: 10000,
        BusinessSector.MANUFACTURE_OF_CONSUMER_ELECTRONICS: 10000,
        BusinessSector.OTHER: 10000,
    }
