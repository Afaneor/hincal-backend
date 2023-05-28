from django.contrib import admin

from server.apps.support.models import Area, Offer, Support


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin[Support]):
    """Класс админки для мер поддержек."""

    list_display = (
        'id',
        'title',
        'is_actual',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'is_actual',
    )
    ordering = (
        'id',
        'title',
        'is_actual',
    )


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin[Offer]):
    """Класс админки для партнерских предложений."""

    list_display = (
        'id',
        'title',
    )
    search_fields = (
        'title',
    )
    ordering = (
        'id',
        'title',
    )


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin[Area]):
    """Класс админки для площадок."""

    list_display = (
        'id',
        'title',
        'territorial_location',
        'site',
    )
    search_fields = (
        'title',
        'territorial_location',
        'site',
    )
    list_filter = (
        'territorial_location',
    )
    ordering = (
        'id',
        'title',
        'territorial_location',
        'site',
    )
