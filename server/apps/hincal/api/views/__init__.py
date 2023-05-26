from server.apps.hincal.api.views.business import BusinessViewSet
from server.apps.hincal.api.views.equipment import EquipmentViewSet
from server.apps.hincal.api.views.business_indicator import BusinessIndicatorViewSet
from server.apps.hincal.api.views.report import ReportViewSet
from server.apps.hincal.api.views.sector import SectorViewSet
from server.apps.hincal.api.views.statistic import StatisticViewSet
from server.apps.hincal.api.views.sub_sector import SubSectorViewSet


__all__ = [
    'SectorViewSet',
    'SubSectorViewSet',
    'BusinessViewSet',
    'EquipmentViewSet',
    'StatisticViewSet',
    'BusinessIndicatorViewSet',
    'ReportViewSet',
]
