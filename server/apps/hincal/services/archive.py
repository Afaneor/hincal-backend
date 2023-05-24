from dataclasses import dataclass


def get_land_cadastral_value():
    """Обертка для сохранения информации в поле модели."""
    return LandCadastralValue().data


def get_property_cadastral_value():
    """Обертка для сохранения информации в поле модели."""
    return LandCadastralValue().data


def get_cost_capital_construction():
    """Обертка для сохранения информации в поле модели."""
    return LandCadastralValue().data


def get_cost_accounting():
    """Обертка для сохранения информации в поле модели."""
    return LandCadastralValue().data


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
class CostCapitalConstruction:
    """Данные по капитальному строительству."""

    data = {
        'lower': 80000,
        'upper': 120000,
    }


@dataclass
class Accounting:
    """Данные по ведению бухгалтерского учета."""

    data = {
        'legal': {
            'osn': {
                'lower': 9000,
                'upper': 40000,
            },
            'ysn': {
                'lower': 7000,
                'upper': 30000,
            },
            'patent': {
                'lower': 0,
                'upper': 0,
            },
        },
        'individual': {
            'osn': {
                'lower': 6000,
                'upper': 35000,
            },
            'ysn': {
                'lower': 5000,
                'upper': 25000,
            },
            'patent': {
                'lower': 5000,
                'upper': 25000,
            },
        },

    }
