"""Файл для router."""
from django.utils.translation import gettext_lazy as _
from rest_framework.routers import APIRootView

from server.apps.support.api.views import (
    AreaViewSet,
    OfferViewSet,
    SupportViewSet,
)
from server.apps.services.custom_router.api_router import ApiRouter


class SupportAPIRootView(APIRootView):
    """Корневой view для апи."""

    __doc__ = _('Приложение поддержки')
    name = _('Поддержка')


router = ApiRouter()
router.APIRootView = SupportAPIRootView

router.register('supports', SupportViewSet, 'supports')
router.register('offers', OfferViewSet, 'offers')
router.register('areas', AreaViewSet, 'areas')
