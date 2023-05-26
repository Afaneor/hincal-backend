from rest_framework.routers import APIRootView

from server.apps.hincal.api.views import (
    BusinessViewSet,
    EquipmentViewSet,
    StatisticViewSet,
    BusinessIndicatorViewSet,
    ReportViewSet,
)
from server.apps.services.custom_router.api_router import ApiRouter


class HincalAPIRootView(APIRootView):
    """Корневой view для app."""

    __doc__ = 'Приложение Hincal'
    name = 'hincal'


router = ApiRouter()

router.APIRootView = HincalAPIRootView
router.register('businesses', BusinessViewSet, 'businesses')
router.register('statistics', StatisticViewSet, 'statistics')
router.register('business-indicator', BusinessIndicatorViewSet, 'business-indicator')
router.register('equipments', EquipmentViewSet, 'equipments')
router.register('reports', ReportViewSet, 'reports')
