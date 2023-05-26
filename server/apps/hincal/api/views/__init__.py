from server.apps.hincal.api.views.business import BusinessViewSet
from server.apps.hincal.api.views.equipment import EquipmentViewSet
from server.apps.hincal.api.views.business_indicator import BusinessIndicatorViewSet
from server.apps.hincal.api.views.report import ReportViewSet
from server.apps.hincal.api.views.statistic import StatisticViewSet


__all__ = [
    'BusinessViewSet',
    'EquipmentViewSet',
    'StatisticViewSet',
    'BusinessIndicatorViewSet',
    'ReportViewSet',
]
