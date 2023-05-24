from django.contrib import admin
from server.apps.hincal.models import Business, Statistic, Indicator, Report


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin[Business]):
    """Бизнес.

    Компании и ИП получаются из DaData.
    Физическое лицо заполняет данные руками.
    """

    list_display = (
        'id',
        'user',
        'type',
        'inn',
        'sector',
        'short_business_name',
    )

    list_filter = (
        'id',
        'type',
        'sector',
        'sub_ector',
    )
    search_fields = (
        'user__email',
        'user__first_name',
        'user_last_name',
        'sector',
        'short_business_name',
        'full_business_name',
        'first_name',
        'last_name',
        'middle_name',
        'address',
        'country',
        'region',
        'city_area',
        'city_district',
        'phone',
        'email',
        'site',
    )
    ordering = (
        'id',
        'name',
        'company',
        'current_stage',
    )


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin[Statistic]):
    """Общая статистика по системе и для пользователя."""

    list_display = (
        'id',
        'user',
    )
    search_fields = (
        'user__email',
        'user__first_name',
        'user_last_name',
    )
    ordering = (
        'id',
        'user',
    )


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin[Indicator]):
    """Экономические показатели ИП, физического лица или компании."""

    list_display = (
        'id',
        'business',
        'year',
    )
    list_filter = (
        'year',
    )
    search_fields = (
        'business__sector',
        'business__short_business_name',
        'business__full_business_name',
        'business__first_name',
        'business__last_name',
        'business__middle_name',
        'business__year',
        'business__address',
    )
    ordering = (
        'id',
        'business',
        'year',
    )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin[Report]):
    """Отчет."""

    list_display = (
        'id',
        'user',
    )
    search_fields = (
        'user__email',
        'user__first_name',
        'user_last_name',
    )
    ordering = (
        'id',
        'user',
    )

