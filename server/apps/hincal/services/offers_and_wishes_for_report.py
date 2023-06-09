from server.apps.hincal.models import Report
from server.apps.support.models import Area, Support, Offer


def add_offers_and_wishes_in_context(report: Report) -> None:
    """Формирование предложений и мер поддержки."""
    report_context = report.context

    if report_context.get('context_for_file').get('offers_and_wishes'):
        return

    areas = ''
    supports = ''
    offers = ''
    for en_index, area in enumerate(Area.objects.filter(tags__in=report.tags.all())[0:2]):  # noqa: E501
        areas += (
            f'Площадка № {en_index + 1}:\a' +
            f"Название: {area.title}\a" +
            f"Адрес: {area.address}\a" +
            f"Подробнее: {area.site}\a"
        )

    for en_index, support in enumerate(Support.objects.filter(tags__in=report.tags.all(), is_actual=True)[0:2]):  # noqa: E501
        supports += (
            f'Мера поддержки № {en_index + 1}:\a' +
            f"Название: {support.title}\a" +
            f"Сумма субсидий: {support.amount}\a" +
            f"Подробнее: {support.site}\a"
        )

    for en_index, offer in enumerate(Offer.objects.filter(tags__in=report.tags.all())[0:2]):  # noqa: E501
        offers += (
            f'Партнерское предложение № {en_index + 1}:\a' +
            f"Название: {offer.title}\a" +
            f"Процентная ставка: {offer.interest_rate}\a" +
            f"Срок займа: {offer.loan_term}\a" +
            f"Сумма займа: {offer.amount}\a" +
            f"Подробнее: {offer.site}\a"
        )

    report_context.get('context_for_file').update(
        {
            'offers_and_wishes': (
                'Площадки для создания промышленного предприятия:\a' +
                areas + '\a\a' +
                'Меры по поддержке промышленных предприятий:\a' +
                supports + '\a\a' +
                'Партнерские предложения по инвестированию:\a' +
                offers + '\a\a'
            ),
        },
    )

    report.context = report_context
    report.save()
