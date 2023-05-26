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


def get_registration_costs():
    """Обертка для сохранения информации в поле модели."""
    return RegistrationCosts().data


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
class RegistrationCosts:
    """Расходы на регистрацию, тыс. руб."""

    data = {
        TypeBusiness.LEGAL: 40,
        TypeBusiness.INDIVIDUAL: 0.8,
    }
