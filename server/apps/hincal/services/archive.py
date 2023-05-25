from dataclasses import dataclass
from decimal import Decimal

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
        'wao': Decimal(15492.36),
        'zao': Decimal(11703.22),
        'zelao': Decimal(4111.5),
        'nao': Decimal(5333.94),
        'sao': Decimal(20532.99),
        'swao': Decimal(19485.33),
        'szao': Decimal(19961.59),
        'tao': Decimal(2890.51),
        'cao': Decimal(63274.79),
        'yuao': Decimal(13510.37),
        'yuwao': Decimal(14086.97),
        'yuzao': Decimal(16423.1),
        'other': Decimal(17233.89),
    }


@dataclass
class PropertyCadastralValue:
    """Данные по кадастровой стоимости имущества."""

    data = {
        'wao': Decimal(15492.36),
        'zao': Decimal(11703.22),
        'zelao': Decimal(4111.5),
        'nao': Decimal(5333.94),
        'sao': Decimal(20532.99),
        'swao': Decimal(19485.33),
        'szao': Decimal(19961.59),
        'tao': Decimal(2890.51),
        'cao': Decimal(63274.79),
        'yuao': Decimal(13510.37),
        'yuwao': Decimal(14086.97),
        'yuzao': Decimal(16423.1),
        'other': Decimal(17233.89),
    }


@dataclass
class Accounting:
    """Данные по ведению бухгалтерского учета."""

    data = {
        'legal': {
            'osn': {
                'lower': Decimal(9000),
                'upper': Decimal(40000),
            },
            'ysn': {
                'lower': Decimal(7000),
                'upper': Decimal(30000),
            },
            'patent': {
                'lower': Decimal(0),
                'upper': Decimal(0),
            },
        },
        'individual': {
            'osn': {
                'lower': Decimal(6000),
                'upper': Decimal(35000),
            },
            'ysn': {
                'lower': Decimal(5000),
                'upper': Decimal(25000),
            },
            'patent': {
                'lower': Decimal(5000),
                'upper': Decimal(25000),
            },
        },

    }


@dataclass
class PossibleIncomeFromPatent:
    data = {
        BusinessSector.FOOD_INDUSTRY: Decimal(10000000),
        BusinessSector.RADIO_ELECTRONICS_AND_INSTRUMENTATION: Decimal(10000000),
        BusinessSector.AVIATION_INDUSTRY: Decimal(10000000),
        BusinessSector.AUTOMOTIVE_INDUSTRY: Decimal(10000000),
        BusinessSector.GENERAL_MECHANICAL_ENGINEERING: Decimal(10000000),
        BusinessSector.LIGHT_INDUSTRY: Decimal(10000000),
        BusinessSector.PRODUCTION_OF_PETROLEUM_PRODUCTS: Decimal(10000000),
        BusinessSector.CHEMICAL_INDUSTRY: Decimal(10000000),
        BusinessSector.PRODUCTION_OF_BUILDING_MATERIALS: Decimal(10000000),
        BusinessSector.PRODUCTION_FOR_MILITARY: Decimal(10000000),
        BusinessSector.PHARMACEUTICAL_INDUSTRY: Decimal(10000000),
        BusinessSector.FUEL_AND_ENERGY_COMPLEX: Decimal(10000000),
        BusinessSector.MEDICAL_INDUSTRY: Decimal(10000000),
        BusinessSector.CABLE_INDUSTRY: Decimal(10000000),
        BusinessSector.WOODWORKING: Decimal(10000000),
        BusinessSector.METALLURGY_AND_METALWORKING: Decimal(10000000),
        BusinessSector.PRINTING_ACTIVITY: Decimal(10000000),
        BusinessSector.PRODUCTION_OF_OTHER_CONSUMER_GOODS: Decimal(10000000),
        BusinessSector.BEVERAGE_PRODUCTION: Decimal(10000000),
        BusinessSector.SCIENTIFIC_ACTIVITY: Decimal(10000000),
        BusinessSector.MACHINE_TOOL_INDUSTRY: Decimal(10000000),
        BusinessSector.SHIPBUILDING: Decimal(10000000),
        BusinessSector.PRODUCTION_OF_RAILWAY_TRANSPORT: Decimal(10000000),
        BusinessSector.MANUFACTURE_OF_CONSUMER_ELECTRONICS: Decimal(10000000),
    }


@dataclass
class RegistrationCosts:
    """Расходы на регистрацию."""

    data = {
        TypeBusiness.LEGAL: Decimal(4000),
        TypeBusiness.INDIVIDUAL: Decimal(800),
    }
