from dataclasses import dataclass

from server.apps.hincal.services.enums import BusinessSector, TypeBusiness


def get_land_cadastral_value():
    """Обертка для сохранения информации в поле модели."""
    return LandCadastralValue().data


def get_property_cadastral_value():
    """Обертка для сохранения информации в поле модели."""
    return LandCadastralValue().data


def get_cost_accounting():
    """Обертка для сохранения информации в поле модели."""
    return LandCadastralValue().data


def get_possible_income_from_patent():
    """Обертка для сохранения информации в поле модели."""
    return PossibleIncomeFromPatent().data


def get_registration_costs():
    """Обертка для сохранения информации в поле модели."""
    return RegistrationCosts().data


@dataclass
class LandCadastralValue:
    """Данные по кадастровой стоимости земли."""

    data = {
        'wao': 15492.36,
        'zao': 11703.22,
        'zelao': 4111.5,
        'nao': 5333.94,
        'sao': 20532.99,
        'swao': 19485.33,
        'szao': 19961.59,
        'tao': 2890.51,
        'cao': 63274.79,
        'yuao': 13510.37,
        'yuwao': 14086.97,
        'yuzao': 16423.1,
        'other': 17233.89,
    }


@dataclass
class PropertyCadastralValue:
    """Данные по кадастровой стоимости имущества."""

    data = {
        'wao': 15492.36,
        'zao': 11703.22,
        'zelao': 4111.5,
        'nao': 5333.94,
        'sao': 20532.99,
        'swao': 19485.33,
        'szao': 19961.59,
        'tao': 2890.51,
        'cao': 63274.79,
        'yuao': 13510.37,
        'yuwao': 14086.97,
        'yuzao': 16423.1,
        'other': 17233.89,
    }


@dataclass
class Accounting:
    """Данные по ведению бухгалтерского учета."""

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
    }


@dataclass
class RegistrationCosts:
    """Расходы на регистрацию."""

    data = {
        TypeBusiness.LEGAL: 40,
        TypeBusiness.INDIVIDUAL: 0.8,
    }
